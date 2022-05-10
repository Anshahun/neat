from celery import Celery
import neat
from neat.conf import celery_config

app = Celery()
app.config_from_object('neat.conf.celery_config')