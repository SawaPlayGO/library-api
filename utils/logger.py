import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


class Logger:
    """
    Класс Logger предоставляет централизованную настройку логирования
    с возможностью включения/отключения логирования в файл.

    Поддерживает вывод в консоль и ротацию логов.
    """

    LOG_DIR = Path("logs")
    LOG_FILE = LOG_DIR / "app.log"

    @classmethod
    def get_logger(cls, name: str = "app", level: int = logging.INFO, log_to_file: bool = True) -> logging.Logger:
        """
        Получить настроенный экземпляр логгера.

        :param name: Имя логгера.
        :param level: Уровень логирования (по умолчанию INFO).
        :param log_to_file: Включить логирование в файл (по умолчанию True).
        :return: Экземпляр логгера.
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        if logger.handlers:
            return logger

        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_to_file:
            cls.LOG_DIR.mkdir(exist_ok=True)

            file_handler = RotatingFileHandler(
                cls.LOG_FILE, maxBytes=1_000_000, backupCount=5, encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

