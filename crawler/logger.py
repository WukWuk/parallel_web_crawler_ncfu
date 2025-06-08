"""
logger.py
----------
Модуль для настройки и работы с логированием краулера.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from crawler.config import LOG_LEVEL

LOG_FILE = "crawler.log"
MAX_LOG_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3  # Сколько старых логов хранить

def setup_logger(name=None):
    """
    Настраивает логгер с выводом в файл и консоль.

    :param name: имя логгера (None — корневой)
    :return: объект логгера
    """
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    # Форматтер для логов
    formatter = logging.Formatter('%(asctime)s [%(processName)s] %(levelname)s: %(message)s')

    # Обработчик для файла с ротацией
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_FILE_SIZE, backupCount=BACKUP_COUNT, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Глобальный логгер, который можно импортировать
log = setup_logger()

# Пример использования:
# from crawler.logger import log
# log.info("Сообщение")
# log.error("Ошибка")

