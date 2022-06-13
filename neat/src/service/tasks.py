from celery import Task
from celery.utils.log import get_task_logger

from neat.conf.config import remote_workspace
from neat import celery_app as app
from neat.src.common.moudles import Server
from neat.src.service.sshclient import SshClient
from neat.src.service.sshclientTask import SshClientTask

logger = get_task_logger(__name__)


def __get_sshclient(host, port, user, password):
    client = SshClient(host, port, user, password)
    return client


@app.task(base=SshClientTask)
def command(server, cmd):
    client: SshClient = command.client(server)
    exit_code, stdout, stderr = client.command(cmd)
    return {'exit_code': exit_code, 'stdout': stdout, 'stderr': stderr}


@app.task(base=SshClientTask)
def scp_env(ip, local_path, remote_path):
    client = scp_env.client(ip)
    client.scp(local_path, remote_path)


@app.task(base=SshClientTask, bind=True)
def exe_script(self: Task, resources, run_command, server: Server, env_command):
    self.update_state(state='PROGRESS', meta={'progress': f'[{server.ip}] connecting to {server.ip} ...'})
    client: SshClient = exe_script.client(server)
    self.update_state(state='PROGRESS', meta={'progress': f'[{server.ip}] scp {resources} to {remote_workspace} ...'})
    client.scp(resources, f'{remote_workspace}')
    self.update_state(state='PROGRESS',
                      meta={'progress': f'[{server.ip}] run command: {env_command} && cd {remote_workspace} '
                                        f'&& {run_command}'})
    exit_code, stdout, stderr = client.command(f'{env_command} && cd {remote_workspace} && {run_command}')
    exit_code = f'[{server.ip}] {exit_code}'
    return {'exit_code': exit_code, 'stdout': stdout, 'stderr': stderr}
