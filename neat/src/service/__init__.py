import os

remote_workspace = '/tmp'
from celery import Celery

#根据需求指定worker执行
app = Celery()
app.config_from_object('neat.src.service.conf.celery_config')

