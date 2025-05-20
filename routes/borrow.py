from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.dependencies import get_user
from database.models import BorrowedBooks, Reader, Book
from database.session import get_db
from database.shemas import BorrowCreate

router = APIRouter(prefix="/borrow", tags=["borrow"])

@router.post("/")
def borrowing(borrow: BorrowCreate, db: Session = Depends(get_db), user: dict = Depends(get_user)) -> dict:
    """
    Выдача книги читателю.

    Аргументы:
        borrow (BorrowCreate): Данные о выдаче книги.
        db (Session): Сессия базы данных.
        user (dict): Авторизованный пользователь (JWT).

    Возвращает:
        dict: Сообщение об успешной выдаче книги.
    """
    reader = db.query(Reader).filter(Reader.id == borrow.reader_id).first()
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    book = db.query(Book).filter(Book.id == borrow.book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    if book.copies is None or book.copies == 0:  # type: ignore
        raise HTTPException(status_code=400, detail="Нет доступных экземпляров книги")
    if db.query(BorrowedBooks).filter(BorrowedBooks.reader_id == reader.id, BorrowedBooks.return_date == None).count() >= 3:
        raise HTTPException(status_code=400, detail="Лимит превышен. Читатель не может взять более 3 книг")
    db_borrow = BorrowedBooks(book_id=book.id, reader_id=reader.id)
    db.add(db_borrow)
    book.copies -= 1  # type: ignore
    db.commit()
    return {"message": "Книга успешно выдана"}

@router.post("/return")
def returning(borrow: BorrowCreate, db: Session = Depends(get_db), user: dict = Depends(get_user)) -> dict:
    """
    Возврат книги читателю.

    Аргументы:
        borrow (BorrowCreate): Данные о возврате книги.
        db (Session): Сессия базы данных.
        user (dict): Авторизованный пользователь (JWT).

    Возвращает:
        dict: Сообщение об успешном возврате книги.
    """
    db_borrow = db.query(BorrowedBooks).filter(
        BorrowedBooks.book_id == borrow.book_id, 
        BorrowedBooks.reader_id == borrow.reader_id,
        BorrowedBooks.return_date == None
    ).first()
    
    if db_borrow is None:
        raise HTTPException(status_code=404, detail="Выдача книги не была найдена")
    
    db_borrow.return_date = datetime.utcnow()  # type: ignore
    book = db.query(Book).filter(Book.id == borrow.book_id).first()
    book.copies += 1  # type: ignore
    db.commit()
    return {"message": "Книга успешно возвращена"}
