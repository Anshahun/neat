from flask import current_app
from flask_wtf import FlaskForm
from typing import List
from wtforms import BooleanField, StringField, PasswordField, validators, FileField, ValidationError, \
    TextAreaField, MultipleFileField, SelectField
from neat.src.app import db
from flask_wtf.file import FileRequired, FileAllowed


class UniqueName(object):
    def __call__(self, form, field):
        posts = db.query_db('select name from tasks where name= ?', (field.data,))
        if len(posts) != 0:
            raise ValidationError(f'Name {field.data} exists')


class TaskForm(FlaskForm):
    # TODO 增加角标
    name = StringField('任务名', [validators.Length(min=4, max=25), UniqueName()])
    script = FileField('脚本', [FileRequired(), FileAllowed(['sh', 'py'], 'Only support [sh, py] extension')])
    command = StringField('启动命令', [validators.DataRequired()])
    env = FileField('环境变量', [FileRequired(), FileAllowed(['yaml'], 'Only support [yaml] extension')])
    note = TextAreaField('备注', render_kw={'cols': 48, 'rows': 8})


def generate_choice(res, key, value):
    for i in res:
        yield i[key], i[value]


def get_service_form(query_tasks, query_servers, query_groups):
    class ServiceForm(FlaskForm):
        task = SelectField('任务', choices=list(generate_choice(query_tasks, 'id', 'name')))
        server = SelectField('服务器', choices=list(generate_choice(query_servers, 'id', 'ip')))
        group = SelectField('服务器组', choices=list(generate_choice(query_groups, 'member', 'name')))
    return ServiceForm()
