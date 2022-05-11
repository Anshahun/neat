import os

import yaml
from celery.app import task
import neat


def load_config():
    with open(neat.config) as f:
        conf = yaml.full_load(f.read())
        print(conf)


if __name__ == '__main__':
    load_config()
