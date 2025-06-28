import logging
import logging.handlers
import os
import sys

current_directory = os.getcwd()


def console_log_handler():
    logStreamFormatter = logging.Formatter(
        fmt=f"%(levelname)-8s %(asctime)s \t %(filename)s @function %(funcName)s line %(lineno)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    consoleHandler = logging.StreamHandler(stream=sys.stdout)
    consoleHandler.setFormatter(logStreamFormatter)
    consoleHandler.setLevel(level=logging.DEBUG)
    return consoleHandler


def file_log_handler(file_name):
    logFileFormatter = logging.Formatter(
        fmt=f"%(levelname)s %(asctime)s (%(relativeCreated)d) \t %(pathname)s F%(funcName)s L%(lineno)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    log_directory = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_directory, exist_ok=True)

    file_path = os.path.join(log_directory, file_name)

    fileHandler = logging.handlers.TimedRotatingFileHandler(
        filename=file_path, when="midnight", interval=1, backupCount=30
    )
    fileHandler.setFormatter(logFileFormatter)
    fileHandler.setLevel(level=logging.INFO)
    return fileHandler


def setup_logger(file_name="recommendation.log"):
    logger = logging.getLogger("standard_logger")
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.propagate = False
    # Attach console handler
    console_handler = console_log_handler()
    logger.addHandler(console_handler)

    file_handler = file_log_handler(file_name)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
