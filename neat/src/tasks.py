from celery.utils.log import get_task_logger

import neat
from neat.src.celeryApp import app
from neat.src.sshclient import SshClient
from neat.src.sshclientTask import SshClientTask

logger = get_task_logger(__name__)


def __get_sshclient(host, port, user, password):
    client = SshClient(host, port, user, password)
    return client


@app.task(base=SshClientTask)
def command(host, port, user, password, cmd):
    client = __get_sshclient(host, port, user, password)
    status = client.command(cmd)
    return status


@app.task(base=SshClientTask)
def scp_env(client: SshClient, ip, remote_path):
    local_path = f"{neat.env_path}/{ip.replace('.', '_')}.conf"
    client.scp(local_path, remote_path)


@app.task(base=SshClientTask)
def scp_script(client: SshClient, filename, remote_path):
    local_path = f"{neat.script_path}/{filename}"
    client.scp(local_path, remote_path)
