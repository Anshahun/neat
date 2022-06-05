from celery.utils.log import get_task_logger

import neat
from neat.src.service.celeryApp import app
from neat.src.service.sshclient import SshClient
from neat.src.service.sshclientTask import SshClientTask

logger = get_task_logger(__name__)


def __get_sshclient(host, port, user, password):
    client = SshClient(host, port, user, password)
    return client


#@app.task(base=SshClientTask)
#def command(ip, cmd):
    # client = __get_sshclient(host, port, user, password)
    #client = command.client(ip)
    #print(client)
    #status = client.command(cmd)
    #return status


@app.task(base=SshClientTask)
def scp_env(ip, local_path, remote_path):
    client = scp_env.client(ip)
    client.scp(local_path, remote_path)


@app.task(base=SshClientTask)
def exe_script(server, env_command, resources, run_command):
    client: SshClient = exe_script.client(server)
    client.scp(resources, f'{neat.remote_workspace}')
    client.command(f'{env_command} && cd {neat.remote_workspace} && {run_command}')
