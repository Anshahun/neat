# neat
**neat**是一个[自动化运维](automation_ops.md)平台

**neat**基于python开发，集成web页面，使批量任务执行更加简单

## Features

## Install
### require
- redis (默认地址：127.0.0.1:6379)
- python 3.8+
### platform
- Linux
  1. 安装venv
  ```shell
  python -m venv venv
  source venv/bin/activate
  ```
  2. 安装neat
  ```shell
  pip install neat-0.1.0-py3-none-any.whl
  ```
  3. 启动flask
  ```shell
  export FLASK_APP=neat
  flask init-db
  flask run
  ```
  4.启动celery
  ```shell
  celery -A neat worker -l INFO
  ```
安装完成后，浏览器访问[http://127.0.0.1:5000](http://127.0.0.1:5000),
创建并提交你的第一个任务吧

## Dependency
### web application framework
- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
  1. [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/)
  2. [WTForms](https://wtforms.readthedocs.io/en/3.0.x/)
- SQLite
### distribute task system
- [Celery](https://docs.celeryq.dev/en/stable/index.html#)
- [Redis](https://redis.io/)
### UI
- [sakura](https://oxal.org/projects/sakura/)
- jQuery
### unit test & code coverage
- [pytest](https://docs.pytest.org/en/7.1.x/)
- [coverage](https://coverage.readthedocs.io/en/6.4.1/)
### package & dependency management
- [poetry](https://python-poetry.org/)
