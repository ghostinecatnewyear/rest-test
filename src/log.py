import logging


def setup(file):
    logging.basicConfig(
        filename=file,
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] %(message)s',
    )


def shutdown():
    logging.shutdown()


def info(message):
    logging.info(message)
