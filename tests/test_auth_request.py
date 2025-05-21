import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from routes.book import read_book
from database.schemas import TokenResponse
from database.models import Book
from main import app


client = TestClient(app)


def test_auth_request():
    """
    Тестирование запроса c аутентификацией (для endpoint /book/read{id}).

    Описание:
        - подменяем зависимости get_db и get_user на магические методы;
        - вызываем функцию read_book с подмененными зависимостями;
        - проверяем, что будет вызвано исключение HTTPException со статусом 200.
    """
    # --- Входные данные ---
    auth_data = TokenResponse(token="test_token")

    # --- Подменяем зависимости ---
    db = MagicMock()
    get_user = MagicMock(return_value=auth_data) # Подменяем зависимость get_user на mock_get_user с возвращаемым значением auth_data
    db.return_value = db
    get_user.return_value = get_user
    book = Book(id=2, title="Торговля и флот", author="Пётр I", year=1706, copies=4)
    db.query().filter().first.side_effect = [book]

    # --- Вызов ---
    response = read_book(book_id=2, db=db, user=get_user)

    # --- Проверка ---
    print(response)
    assert response is not None


def test_not_auth_request_api():
    """
    Тестирование запроса без аутентификации (для endpoint /book/read{id}).
    """
    response = client.get("/book/read/2")
    assert response.status_code == 401