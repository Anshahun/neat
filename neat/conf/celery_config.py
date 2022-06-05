broker_url = 'redis://127.0.0.1:6379'
result_backend = 'redis://127.0.0.1:6379'
imports = ['neat.src.service.tasks', ]
accept_content = ['pickle']
result_serializer = 'pickle'
#event_serializer = 'pickle'
task_serializer = 'pickle'
