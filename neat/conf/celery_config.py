broker_url = 'redis://10.10.26.59:6379'
result_backend = 'redis://10.10.26.59:6379'
imports = ['neat.src.tasks', ]
accept_content = ['pickle']
result_serializer = 'pickle'
#event_serializer = 'pickle'
task_serializer = 'pickle'
