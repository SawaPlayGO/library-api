import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock

from routes.borrow import borrowing
from database.schemas import BorrowCreate, TokenResponse
from database.models import Reader, Book

def test_borrowing_limit_exceeded():
    """
    Тестирует, что читатель не может взять более 3 книг одновременно.
    """
    # --- Входные данные ---
    borrow_data = BorrowCreate(reader_id=2, book_id=2)

    # --- Мок БД сессии ---
    db = MagicMock()

    # --- Мокаем Reader ---
    mock_reader = Reader(id=2, name="Тест", email="test@test.com")
    mock_get_user = MagicMock(return_value=TokenResponse(token="test_token")) # Подменяем зависимость get_user на mock_get_user с возвращаемым значением auth_data
    db.query().filter().first.side_effect = [mock_reader, Book(id=2, title="Торговля и флот", author="Пётр I", year=1706, copies=4)] # Создаем книгу с 4 экземплярами

    # Мокаем количество уже взятых книг = 3 (превышает лимит)
    db.query().filter().count.return_value = 3

    # --- Вызов ---
    with pytest.raises(HTTPException) as exc_info:
        borrowing(borrow_data, db=db, user=mock_get_user)

    # --- Проверка ---
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Лимит превышен. Читатель не может взять более 3 книг"
