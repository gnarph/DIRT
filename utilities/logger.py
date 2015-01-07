import logging


def get_logger():
    return logging.getLogger('dirt')


def show_info():
    level = logging.INFO
    logging.basicConfig(level=level)
    logger = get_logger()
    logger.setLevel(level)


def info(msg):
    logger = get_logger()
    logger.info(msg)