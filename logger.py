import logging
import os
from datetime import datetime

def setup_logger(logger_name=None):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    log_filename = datetime.now().strftime('logs/kannada_nudi_%d_%m_%y.log')
    if logger_name is not None:
        logger = logging.getLogger(name=logger_name)
    else:
        logger = logging.getLogger(name=__name__)

    logger.handlers = []
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

    #create file handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger