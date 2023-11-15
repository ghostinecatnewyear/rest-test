import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='path to .ini config file')
    args = parser.parse_args()

    return args.config
