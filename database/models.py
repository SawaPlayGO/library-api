from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .session import Base


class User(Base):
    """
    Модель пользователя для базы данных.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        email (str): Электронная почта пользователя, уникальная и обязательная.
        password_hash (str): Хэш пароля пользователя, обязательный.
        created_at (str): Дата и время создания пользователя, по умолчанию текущее время.

    Методы:
        __repr__(): Возвращает строковое представление объекта пользователя.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(String, default=datetime.utcnow)

    def __repr__(self):
        return f'<User(email={self.email!r}, created_at={self.created_at!r})>'

