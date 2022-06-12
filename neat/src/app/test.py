class Person(object):
    def __init__(self):
        self.a = 1
        print('init...')

    def __call__(self, *args):
        print('call...')

def _generate_env_command(env):
    print(env)
    for key in env:
        yield f'export {key}={env[key]}'

if __name__ == '__main__':
    li = [{'mysql_ip': '10.183.29.1'}, {'abc': 'bcd'}]
    l = list(_generate_env_command(li))
    print(l)

