import logging


def get_logger():
    """
    Get DIRT's logger
    """
    return logging.getLogger('dirt')


def show_info():
    """
    Show info level logger output
    """
    level = logging.INFO
    logging.basicConfig(level=level)
    logger = get_logger()
    logger.setLevel(level)


def info(msg):
    """
    Log msg to info level
    """
    logger = get_logger()
    logger.info(msg)