import logging

logging.basicConfig(filename="events.log",
                             filemode="a",
                             format="%(levelname)s at %(asctime)s :: %(message)s",
                             level=logging.INFO)

logger = logging.getLogger()

def debug(msg):
    logger.debug(msg)

def info(msg):
    logger.info(msg)

def warning(msg):
    logger.warning(msg)

def error(msg):
    logger.error(msg)

def critical(msg):
    logger.critical(msg)