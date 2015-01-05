import logging


def get_logger():
    return logging.getLogger('dirt')


def show_info():
    logging.basicConfig(level=logging.INFO)


def info(msg):
    logger = get_logger()
    logger.info(msg)