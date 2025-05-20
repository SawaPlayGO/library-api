from fastapi import Header, HTTPException, status
from jose.exceptions import JWTError
from typing import Optional

from .jwt import jwt_handler

def get_user(authorization: Optional[str] = Header(default=None)) -> dict:
    """
    Возвращает информацию о текущем пользователе, если он авторизован.

    :param authorization: Заголовок Authorization, который может быть None
    :return: Информация о пользователе, если он авторизован
    :raises HTTPException: 401, если пользователь не авторизован
    """
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")

    token = authorization.split(" ")[1]
    try:
        payload = jwt_handler.verify_token(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return payload

