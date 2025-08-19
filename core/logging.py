import logging
import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

LOG_LEVEL_MAPPING = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

def setup_logging():
    logger = logging.getLogger("my_embedding_api")
    logger.setLevel(LOG_LEVEL_MAPPING.get(LOG_LEVEL, logging.INFO))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL_MAPPING.get(LOG_LEVEL, logging.INFO))

    formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] [%(name)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger
