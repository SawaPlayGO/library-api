from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from database.models import User
from database.shemas import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(register_user: UserCreate, db: Session = Depends(get_db)) -> User:
    """
    Обрабатывает регистрацию пользователя.

    Создает нового пользователя на основе предоставленных данных регистрации и проверяет уникальность электронной почты.

    Аргументы:
        register_user (UserCreate): Данные регистрации пользователя.
        db (Session): Сессия базы данных. По умолчанию Depends(get_db).

    Возвращает:
        User: Новый созданный пользователь.

    Вызывает исключение:
        HTTPException: Если предоставленная электронная почта уже существует.
    """
    if db.query(User).filter(User.email == register_user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(**register_user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
