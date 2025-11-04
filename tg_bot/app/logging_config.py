import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger(name, log_file, level=logging.DEBUG):
    """Настройка логгера для модуля"""
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=2, encoding='utf-8')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False  # Отключаем распространение логов
    logging.getLogger('werkzeug').disabled = True

    return logger