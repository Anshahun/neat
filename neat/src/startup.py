import os

import yaml
from celery import chain

import neat
from neat.src.tasks import command


def load_config(conf):
    with open(conf) as f:
        conf = yaml.full_load(f.read())
        return conf


def generate_env_config(args):
    for i in args:
        for ip, arg in i.items():
            with open(f"{neat.env_path}/{ip.replace('.', '_')}.conf", 'w') as f:
                for key, value in arg.items():
                    f.write(f'{key}={value}\n')


if __name__ == '__main__':
    neat_conf = load_config(neat.neat_conf)
    server_conf = load_config(neat.server_conf)
    server = server_conf[0]
    res = command.delay(server['ip'], server['port'], server['user'], server['password'], 'echo 1')
    print(res.get())
    generate_env_config(neat_conf['neat']['argument'])
    ip = 'a.b.c'
    print(ip.replace('.', '_'))
