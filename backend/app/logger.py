import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name, log_file='', level=logging.INFO):
    # base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # logs_dir = os.path.join(base_dir, 'logs')
    #
    # os.makedirs(logs_dir, exist_ok=True)
    #
    # log_path = os.path.join(logs_dir, log_file)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # handler = RotatingFileHandler(
    #     # log_path,
    #     log_file,
    #     maxBytes=10 * 1024 * 1024,  # 10 MB
    #     backupCount=3,
    #     encoding='utf-8'
    # )
    # handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.handlers.clear()

    # logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

