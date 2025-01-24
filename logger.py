# logger.py

import logging
from logging.handlers import RotatingFileHandler
import os

class Logger:
    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._logger is None:
            self._logger = self._setup_logger()

    def _setup_logger(self):
        # 创建logger对象
        logger = logging.getLogger('bot_logger')
        logger.setLevel(logging.DEBUG)

        # 避免重复添加handler
        if logger.handlers:
            return logger

        # 创建日志目录
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # 文件处理器（带轮转）
        file_handler = RotatingFileHandler(
            filename=os.path.join(log_dir, 'bot.log'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)

        # 错误日志文件处理器
        error_file_handler = RotatingFileHandler(
            filename=os.path.join(log_dir, 'error.log'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        error_file_handler.setLevel(logging.ERROR)

        # 日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 设置格式
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        error_file_handler.setFormatter(formatter)

        # 添加处理器
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(error_file_handler)

        return logger

    def debug(self, message):
        self._logger.debug(message)

    def info(self, message):
        self._logger.info(message)

    def warning(self, message):
        self._logger.warning(message)

    def error(self, message, exc_info=False):
        self._logger.error(message, exc_info=exc_info)

    def critical(self, message):
        self._logger.critical(message)

# 创建全局logger实例
logger = Logger()