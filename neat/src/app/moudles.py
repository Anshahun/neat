import os

from neat.src.app import tasks_folder


class ServiceTask(object):
    def __init__(self, name, command, env_name, script_name, notes):
        self.name = name
        self.command = command
        self.env = f'{tasks_folder}/{self.name}/env/{env_name}'
        self.script = f'{tasks_folder}/{self.name}/bin/{script_name}'
        self.notes = notes

    def init_task(self):
        os.makedirs(f'{tasks_folder}/{self.name}/bin', exist_ok=True)
        os.makedirs(f'{tasks_folder}/{self.name}/env', exist_ok=True)
        with open(f'{tasks_folder}/{self.name}/startup.sh', 'w') as f:
            f.write('#! /bin/bash\n')
            f.write(f'{self.command}\n')


class Server(object):

    def __init__(self, ip, port, user, password):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
