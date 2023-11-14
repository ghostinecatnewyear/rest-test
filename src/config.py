import configparser


def parse(file):
    config = configparser.ConfigParser()
    if not config.read(file):
        raise Exception(f"failed to find/open config file '{file}'")

    return config
