import os

project_dir = os.path.dirname(__file__)
neat_conf = os.path.join(project_dir, 'conf/neat.yaml')
server_conf = os.path.join(project_dir, 'conf/server.yaml')
env_path = os.path.join(project_dir, 'tmp')
script_path = os.path.join(project_dir, 'script')
remote_workspace = '/tmp'
remote_config_name = 'neat.conf'
#celery_config = 'neat.conf.celery_config.py'

