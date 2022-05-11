from celery import Celery
import neat
from neat.conf import celery_config

#根据需求指定worker执行
app = Celery()
app.config_from_object('neat.conf.celery_config')