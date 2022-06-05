import yaml
from flask import app

import neat


def load_config(conf):
    with open(conf) as f:
        conf = yaml.full_load(f.read())
        return conf


def generate_env_config(args):
    config_dict = {}
    for i in args:
        for ip, arg in i.items():
            config_path = f"{neat.env_path}/{ip.replace('.', '_')}.conf"
            with open(config_path, 'w') as f:
                for key, value in arg.items():
                    print(f'export {key}={value}\n')
                    f.write(f'export {key}={value}\n')
            config_dict[ip] = config_path
    return config_dict



    # for script in neat_conf['neat']['tasks']:
    #   if script['name'] == script_name:
    #      config_dict = generate_env_config(script['argument'])
    #     res = exe_script.delay(target, config_dict[target], script['resources'], script['command'])
    #    print(res.get())


if __name__ == '__main__':
    neat_conf = load_config(neat.neat_conf)
    server_conf = load_config(neat.server_conf)
    server = server_conf[0]
    # res = command.delay(server['ip'], 'touch a.txt')
    # print(res.get())
    # generate_env_config(neat_conf['neat']['argument'])
    print(neat_conf)
    #distribute_execute('172.16.135.183', 'test', neat_conf)
    # res = scp_env.delay(server['ip'],f'{neat.env_path}/test1.conf', '~/test1.conf')
    # scp_env.delay(server['ip'], f'{neat.script_path}/test1.sh', './')
    # res = command.delay(server['ip'], 'sh test1.sh')
    # print(res.get())
