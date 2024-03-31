import logging
import os

log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)


def setup_logger(filename, level=logging.INFO):
    log_file = os.path.join(log_directory, f"{filename}.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(filename)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
