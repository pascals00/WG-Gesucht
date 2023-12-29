from .constants import LOG_PATH
import logging


def setup_logging(): 
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_PATH, mode='w'),
            logging.StreamHandler()
        ]
    )