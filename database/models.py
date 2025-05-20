from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
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
    

class Book(Base):
    """
    Модель книги для базы данных.

    Атрибуты:
        id (int): Уникальный идентификатор книги.
        title (str): Название книги, обязательное поле.
        author (str): Автор книги, обязательное поле.
        year (int): Год издания книги, необязательное поле.
        isbn (str): ISBN книги, уникальное поле, необязательное поле.
        copies (int): Количество экземпляров книги, по умолчанию 1, необязательное поле.

    Методы:
        __repr__(): Возвращает строковое представление объекта книги.
    """
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    isbn = Column(String, unique=True, nullable=True)
    copies = Column(Integer, nullable=False, default=1, server_default='1')

    def __repr__(self):
        return f'<Book(title={self.title!r}, author={self.author!r}, year={self.year!r}, isbn={self.isbn!r}, copies={self.copies!r})>'
    

class Reader(Base):
    """
    Модель читателя для базы данных.

    Атрибуты:
        id (int): Уникальный идентификатор читателя.
        name (str): Имя читателя, обязательное поле.
        email (str): Электронная почта читателя, уникальное поле, обязательное поле.

    Методы:
        __repr__(): Возвращает строковое представление объекта читателя.
    """

    __tablename__ = 'readers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f'<Reader(name={self.name!r}, email={self.email!r})>'


class BorrowedBooks(Base):
    """
    Модель для хранения информации о выданных книгах.

    Атрибуты:
        id (int): Уникальный идентификатор выдачи книги.
        book_id (int): Идентификатор выданной книги.
        reader_id (int): Идентификатор читателя, получившего книгу.
        borrow_date (datetime): Дата выдачи книги.
        return_date (datetime): Дата возврата книги (изначально None).

    Методы:
        __repr__(): Возвращает строковое представление объекта выдачи книги.
    """
    __tablename__ = 'borrowed_books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    reader_id = Column(Integer, ForeignKey('readers.id'), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)

    def __repr__(self):
        return f'<BorrowedBooks(book_id={self.book_id!r}, reader_id={self.reader_id!r}, borrow_date={self.borrow_date!r}, return_date={self.return_date!r})>'
