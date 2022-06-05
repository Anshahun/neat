import os

from flask import Flask
from neat.src.app import db

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

tasks_folder = f"{app.root_path}/tasks"
app.config.from_pyfile('config.py', silent=True)

try:
    os.makedirs(app.instance_path)
    os.makedirs(tasks_folder)
    # ensure the folder exists
except OSError:
    pass

db.init_app(app)

#必须使用lazy import,否则会有循环引用问题
from neat.src.app import portal
app.register_blueprint(portal.bp)


