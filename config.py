import os
from dotenv import load_dotenv

from utils.logger import Logger

load_dotenv('.env')


class Settings:
    """Класс для хранения настроек приложения"""

    def __init__(self):
        self.PROJECT_NAME = "Library API"
        self.LOG_FILE = bool(os.getenv("LOG_FILE", "app.log"))
        self.logger = Logger.get_logger(__name__, log_to_file=self.LOG_FILE)

        # JWT
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

        # БД
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_PORT = os.getenv("DB_PORT", "5432")
        self.DB_NAME = os.getenv("DB_NAME", "library")
        self.DB_USER = os.getenv("DB_USER", "postgres")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

        self.SQLALCHEMY_DATABASE_URL = (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

        # SQL логирование
        self.ECHO_SQL = bool(os.getenv("ECHO_SQL", False))

        # Лимит использования API (/books, /auth/..)
        self.RATE_LIMITER = str(os.getenv("RATE_LIMITER", "10"))

        # Пример логирования
        self.logger.info(f"SQLALCHEMY_DATABASE_URL: {self.SQLALCHEMY_DATABASE_URL}")


settings = Settings()
