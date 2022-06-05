from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from neat.src.app import db
from neat.src.app.db import get_db
from neat.src.app.moudles import ServiceTask, Server
from neat.src.app.validate import form
from neat.src.app.validate.form import TaskForm
from neat.src.service.startup import load_config


bp = Blueprint('portal', __name__)


@bp.route('/', methods=('POST', 'GET'))
def index():
    tasks = db.query_db('select id, name, notes from tasks')
    servers = db.query_db('select id, ip from servers')
    groups = db.query_db('select name,group_concat(server_id) as member from groups group by name order by name')
    service_form = form.get_service_form(tasks, servers, groups)
    if request.method == 'POST' and service_form.validate_on_submit():
        task_id = service_form.task.data
        server_id = service_form.server.data
        distribute_execute(task_id, server_id)
        return render_template('index.html', form=service_form, tasks=tasks)
    else:
        return render_template('index.html', form=service_form, tasks=tasks)


def _generate_env_command(env):
    print(env)
    for key in env:
        yield f'export {key}={env[key]}'


def distribute_execute(task_id, server_id):
    task = db.query_db('select name, command, env, script from tasks where id = ?', (task_id,), one=True)
    query_server = db.query_db('select ip,port,user,password from servers where id = ?', (server_id,), one=True)
    if task is None or query_server is None:
        print(None)
    else:
        server = Server(query_server['ip'], query_server['port'], query_server['user'], query_server['password'])
        env_conf = load_config(task['env'])[query_server['ip']]
        print(env_conf)
        env_command = ' && '.join(list(_generate_env_command(env_conf)))
        from neat.src.service.tasks import exe_script
        res = exe_script.delay(server, env_command, task['script'], task['command'])
        print(res.get(timeout=15))


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
