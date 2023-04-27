import logging

logging.basicConfig(level=logging.DEBUG)


def get_logger(LOGGING_NAME=None):
    return logging.getLogger(LOGGING_NAME)
