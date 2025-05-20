from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.dependencies import get_user
from database.models import Reader
from database.session import get_db
from database.shemas import ReaderCreate, ReaderUpdate

router = APIRouter(prefix="/reader", tags=["reader"])


@router.post("/create")
def create_reader(reader: ReaderCreate, db: Session = Depends(get_db), user: dict = Depends(get_user)) -> dict:
    """Создание нового читателя.

    Аргументы:
        reader (ReaderCreate): Данные читателя.
        db (Session): Сессия базы данных.
        user (dict): Авторизованный пользователь (JWT).

    Возвращает:
        dict: Сообщение об успешном создании.
    """
    if db.query(Reader).filter(Reader.email == reader.email).first():
        raise HTTPException(status_code=400, detail="Email уже существует")
    new_reader = Reader(
        name=reader.name,
        email=reader.email
    )
    db.add(new_reader)
    db.commit()
    db.refresh(new_reader)

    return {"message": "Читатель успешно создан", "reader_id": new_reader.id}


@router.get("/read/{reader_id}", response_model=ReaderCreate)
def read_reader(reader_id: int, db: Session = Depends(get_db), user: dict = Depends(get_user)) -> ReaderCreate:
    """Получение информации о читателе.

    Аргументы:
        reader_id (int): Идентификатор читателя.
        db (Session): Сессия базы данных.
        user (dict): Авторизованный пользователь (JWT).

    Возвращает:
        dict: Информация о читателе.
    """
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return ReaderCreate(**reader.__dict__)


@router.put("/update/{reader_id}")
def update_reader(reader_id: int, reader: ReaderUpdate, db: Session = Depends(get_db), user: dict = Depends(get_user)) -> dict:
    """Обновление информации о читателе.

    Аргументы:
        reader_id (int): Идентификатор читателя.
        reader (ReaderUpdate): Данные читателя.
        db (Session): Сессия базы данных.
        user (dict): Авторизованный пользователь (JWT).

    Возвращает:
        dict: Сообщение об успешном обновлении.
    """
    db_reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")

    if reader.name is not None:
        db_reader.name = reader.name  # type: ignore
    if reader.email is not None:
        db_reader.email = reader.email  # type: ignore

    db.commit()
    return {"message": "Читатель успешно обновлен"}


@router.delete("/delete/{reader_id}")
def delete_reader(reader_id: int, db: Session = Depends(get_db), user: dict = Depends(get_user)) -> dict:
    """Удаление читателя.

    Аргументы:
        reader_id (int): Идентификатор читателя.
        db (Session): Сессия базы данных.
        user (dict): Авторизованный пользователь (JWT).

    Возвращает:
        dict: Сообщение об успешном удалении.
    """
    db_reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if db_reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    db.delete(db_reader)
    db.commit()
    return {"message": "Читатель успешно удален"}
