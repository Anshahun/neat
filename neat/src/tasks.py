from celery.utils.log import get_task_logger

from neat.src.celeryApp import app
from neat.src.sshclient import SshClient
from neat.src.sshclientTask import SshClientTask

logger = get_task_logger(__name__)


@app.task
def get_sshclient(host, port, user, password):
    client = SshClient(host, port, user, password)
    return client


@app.task(base=SshClientTask)
def command():
    res = command.test('abc')
    print(res)
