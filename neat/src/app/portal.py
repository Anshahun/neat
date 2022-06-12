from celery import states
from celery.canvas import group
from celery.result import GroupResult
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from neat.src.app import db
from neat.src.app.moudles import ServiceTask, Server
from neat.src.app.validate import form
from neat.src.app.validate.form import TaskForm
from neat.src.service import app
from neat.src.service.startup import load_config

bp = Blueprint('portal', __name__)


@bp.route('/', methods=('POST', 'GET'))
def index():
    tasks = db.query_db('select id, name, notes from tasks')
    servers = db.query_db('select id, ip from servers')
    groups = db.query_db('select name,group_concat(server_id) as member from groups group by name order by name')
    service_form = form.get_service_form(tasks, servers, groups)
    return render_template('index.html', form=service_form, tasks=tasks)


@bp.route('/submit_task', methods=('POST',))
def submit_task():
    tasks = db.query_db('select id, name, notes from tasks')
    servers = db.query_db('select id, ip from servers')
    groups = db.query_db('select name,group_concat(server_id) as member from groups group by name order by name')
    service_form = form.get_service_form(tasks, servers, groups)
    if service_form.validate_on_submit():
        task_id = service_form.task.data
        server_ids = service_form.group.data
        res = distribute_execute(task_id, server_ids.split(','))
        return {'celery_task_id': res.id}


@bp.route('/monitor_task', methods=('POST',))
def monitor_task():
    celery_task_id = request.form['celery_task_id']
    print(f'{celery_task_id}===========================')
    post = list(__generate_task_result(GroupResult.restore(celery_task_id, app=app)))
    return {'results': post}


def __generate_task_result(res: GroupResult):
    for result in res.results:
        if result.status == states.FAILURE:
            post = {'status': result.status, 'traceback': result.traceback}
        elif result.status == states.SUCCESS:
            post = {'status': result.status, 'exit_code': result.result['exit_code'],
                    'stdout': result.result['stdout'], 'stderr': result.result['stderr']}
        else:
            post = {'status': result.status, 'result': result.result}
        yield post


def __generate_env_command(env):
    for key in env:
        yield f'export {key}={env[key]}'


def __generate_task_env(task, query_servers):
    for query_server in query_servers:
        server = Server(query_server['ip'], query_server['port'], query_server['user'], query_server['password'])
        env_conf = load_config(task['env'])[query_server['ip']]
        env_command = ' && '.join(list(__generate_env_command(env_conf)))
        yield {'server': server, 'env_conf': env_conf, 'env_command': env_command}


def distribute_execute(task_id, server_ids):
    ids = ''
    for id in server_ids:
        ids = ids + f"{id},"
    ids = ids[:-1]
    task = db.query_db('select name, command, env, script from tasks where id = ?', (task_id,), one=True)
    query_servers = db.query_db(f'select ip,port,user,password from servers where id in ( {ids} )')
    print(task)
    print(query_servers)
    if task is None or query_servers is None:
        return None
    else:
        from neat import exe_script
        print(list(__generate_task_env(task, query_servers)))
        g: GroupResult = group(exe_script.s(task['script'], task['command'], task_env['server'], task_env['env_command'])
                               for task_env in list(__generate_task_env(task, query_servers)))()
        g.save(backend=app)
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


@bp.route("/add", methods=('POST', 'GET'))
def add():
    a = request.form.get("a", 0, type=float)
    b = request.form.get("b", 0, type=float)
    return {'result': a + b}
