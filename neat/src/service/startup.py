import yaml


def load_config(conf):
    with open(conf) as f:
        conf = yaml.full_load(f.read())
        return conf
