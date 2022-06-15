import yaml
from celery import states
from celery.canvas import group
from celery.result import GroupResult, AsyncResult
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from neat.src.app import db, form
from neat.src.common.moudles import ServiceTask, Server
from neat.src.app.form import TaskForm

bp = Blueprint('portal', __name__)


@bp.route('/', methods=('POST', 'GET'))
def index():
    tasks = db.query_db('select id, name, notes from tasks')
    servers = db.query_db('select id, ip from servers')
    groups = db.query_db('select name,group_concat(server_id) as member from groups group by name order by name')
    service_form = form.get_service_form(tasks, servers, groups)
    if request.method == 'POST' and service_form.validate_on_submit():
        task_id = service_form.task.data
        server_ids = ''
        if service_form.type.data == 'group':
            server_ids = service_form.group.data
        elif service_form.type.data == 'single':
            server_ids = service_form.server.data
        group_result = distribute_execute(task_id, server_ids)
        execute_ids = list(__generate_execute_ids(group_result))
        return render_template('task_result.html', execute_ids=execute_ids)
    else:
        return render_template('index.html', form=service_form, tasks=tasks)


@bp.route('/monitor_task', methods=('POST',))
def monitor_task():
    execute_id = request.form['execute_id']
    from neat import celery_app
    result = AsyncResult(execute_id, app=celery_app)
    post = __generate_task_result(result)
    return post


def __load_config(conf):
    with open(conf) as f:
        conf = yaml.full_load(f.read())
        return conf


def __generate_execute_ids(res: GroupResult):
    for result in res.results:
        yield result.id


def __generate_task_result(result: AsyncResult):
    if result.status == states.FAILURE:
        post = {'status': result.status, 'traceback': result.traceback}
    elif result.status == states.SUCCESS:
        post = {'status': result.status, 'exit_code': result.result['exit_code'],
                'stdout': result.result['stdout'], 'stderr': result.result['stderr']}
    else:
        post = {'status': result.status, 'result': result.result}
    return post


def __generate_env_command(env):
    for key in env:
        yield f'export {key}={env[key]}'


def __generate_task_env(task, query_servers):
    for query_server in query_servers:
        server = Server(query_server['ip'], query_server['port'], query_server['user'], query_server['password'])
        env_conf = __load_config(task['env'])[query_server['ip']]
        env_command = ' && '.join(list(__generate_env_command(env_conf)))
        yield {'server': server, 'env_conf': env_conf, 'env_command': env_command}


def distribute_execute(task_id, server_ids):
    task = db.query_db('select name, command, env, script from tasks where id = ?', (task_id,), one=True)
    query_servers = db.query_db(f'select ip,port,user,password from servers where id in ( {server_ids} )')
    print(task)
    print(query_servers)
    if task is None or query_servers is None:
        return None
    else:
        from neat.src.service.tasks import exe_script
        print(list(__generate_task_env(task, query_servers)))
        g: GroupResult = group(
            exe_script.s(task['script'], task['command'], task_env['server'], task_env['env_command'])
            for task_env in list(__generate_task_env(task, query_servers)))()
        from neat import celery_app
        g.save(backend=celery_app.backend)
        return g


@bp.route('/create_task', methods=('POST', 'GET'))
def create_task():
    form = TaskForm()
    if request.method == 'POST' and form.validate_on_submit():
        task = ServiceTask(form.name.data, form.command.data, secure_filename(form.env.data.filename),
                           secure_filename(form.script.data.filename), form.note.data)
        task.init_task()
        form.env.data.save(task.env)
        form.script.data.save(task.script)
        db.update_db('insert into tasks (name, command, env, script, notes) values (?, ?, ?, ?, ?)',
                     (task.name, task.command, task.env, task.script, task.notes))
        return redirect(url_for('portal.index'))
    else:
        return render_template('create_task.html', form=form)
