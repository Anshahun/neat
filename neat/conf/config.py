#celery config
import os

broker_url = 'redis://127.0.0.1:6379'
result_backend = 'redis://127.0.0.1:6379'
imports = ['neat.src.service.tasks', ]
accept_content = ['pickle']
result_serializer = 'pickle'
task_serializer = 'pickle'

#falsk config
SECRET_KEY = os.environ.get('SECRET_KEY') or 'fjdlj324fs5ssjflKzcznv*c'

#common
remote_workspace = '/tmp'
