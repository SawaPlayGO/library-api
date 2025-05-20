from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from utils.dependencies import get_user
from database.models import Book
from database.session import get_db
from database.shemas import BookCreate, BookResponse, BookUpdate
from utils.rate_limiter import limiter
from config import settings

router = APIRouter(prefix="/book", tags=["book"])


@router.post("/create")
def create_book(book: BookCreate, db: Session = Depends(get_db), user: dict = Depends(get_user)) -> dict:
    """
    Создание новой книги.

    Аргументы:
        book (BookCreate): Данные книги.
        db (Session): Сессия базы данных.
        user (dict): Авторизованный пользователь (JWT).

    Возвращает:
        dict: Сообщение об успешном создании.
    """
    new_book = Book(
        title=book.title,
        author=book.author,
        year=book.year,
        isbn=book.isbn,
        copies=book.copies
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {"message": "Книга успешно создана", "book_id": new_book.id}

@router.get('/read/{book_id}', response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db), user: dict = Depends(get_user)) -> BookResponse:
    """
    Получение информации о книге.

    Аргументы:
        book_id (int): Идентификатор книги.
        db (Session): Сессия базы данных.
        user (dict): Авторизованный пользователь (JWT).

    Возвращает:
        dict: Информация о книге.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return BookResponse(**book.__dict__)

@router.put('/update/{book_id}')
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db), user: dict = Depends(get_user)) -> dict:
    """
    Обновление информации о книге.

    Аргументы:
        book_id (int): Идентификатор книги.
        book (BookCreate): Данные книги.
        db (Session): Сессия базы данных.
        user (dict): Авторизованный пользователь (JWT).

    Возвращает:
        dict: Сообщение об успешном обновлении.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    if book.title is not None:
        db_book.title = book.title # type: ignore
    if book.author is not None:
        db_book.author = book.author # type: ignore
    if book.year is not None:
        db_book.year = book.year # type: ignore
    if book.isbn is not None:
        db_book.isbn = book.isbn # type: ignore
    if book.copies is not None:
        db_book.copies = book.copies # type: ignore
    db.commit()
    return {"message": "Книга успешно обновлена"}

@router.delete('/delete/{book_id}')
def delete_book(book_id: int, db: Session = Depends(get_db), user: dict = Depends(get_user)) -> dict:
    """
    Удаление книги.

    Аргументы:
        book_id (int): Идентификатор книги.
        db (Session): Сессия базы данных.
        user (dict): Авторизованный пользователь (JWT).

    Возвращает:
        dict: Сообщение об успешном удалении.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    db.delete(db_book)
    db.commit()
    return {"message": "Книга успешно удалена"}

@router.get('/all')
@limiter.limit(f"{settings.RATE_LIMITER}/minute")
def get_books(request: Request, db: Session = Depends(get_db)) -> List[BookResponse]:
    """
    Получение списка всех книг.

    Аргументы:
        db (Session): Сессия базы данных.
        user (dict): Авторизованный пользователь (JWT).

    Возвращает:
        List[BookResponse]: Список книг.
    """
    books = db.query(Book).all()
    return [BookResponse(**book.__dict__) for book in books]