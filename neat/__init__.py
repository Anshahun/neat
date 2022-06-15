import os
from celery import Celery
from flask import Flask
from neat.src.app import db

flask_app = Flask(__name__, instance_relative_config=True)
flask_app.config.from_mapping(
    DATABASE=os.path.join(flask_app.instance_path, 'neat.sqlite'),
)
#app.config.from_pyfile()

tasks_folder = f"{flask_app.root_path}/tasks"
config_folder = f"{flask_app.root_path}/conf"
flask_app.config.from_pyfile(f'{config_folder}/config.py')
try:
    os.makedirs(flask_app.instance_path)
    os.makedirs(tasks_folder)
    # ensure the folder exists
except OSError:
    pass

db.init_app(flask_app)

#必须使用lazy import,否则会有循环引用问题
from neat.src.app import portal
flask_app.register_blueprint(portal.bp)

celery_app = Celery()
celery_app.config_from_object(f'neat.conf.config')


