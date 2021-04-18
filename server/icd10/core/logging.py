import logging
import logging.handlers
import os
import datetime

log_level_map = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

log_level_str = os.getenv("LOG_LEVEL", "DEBUG")
enable_file_handler = os.getenv("EN_FILE_LOG", "True")

log_level = log_level_map.get(log_level_str, logging.INFO)

logger = logging.getLogger("MedicalExtraction")
logger.propagate = False
logger.setLevel(log_level)

formatter = logging.Formatter('%(module)s:%(funcName)s:%(lineno)d:%(name)s:%(levelname)s:%(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(log_level)
logger.addHandler(stream_handler)

if (enable_file_handler == "True"):
    file_handler = logging.FileHandler(
        datetime.datetime.now().strftime(
            'logs/{}%d_%m_%Y %H_%M.log'.format("CareerMD")
        ),
        mode='w'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


