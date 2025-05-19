from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database.session import get_db
from database.models import User
from database.shemas import UserCreate, TokenResponse
from utils.jwt import JWT
from config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
jwt = JWT(secret_key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


@router.post("/register", response_model=TokenResponse)
def register(register_user: UserCreate, db: Session = Depends(get_db)) -> TokenResponse:
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

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(register_user.password)
    user = User(email=register_user.email, password_hash=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    response = TokenResponse(token=jwt.generate_token({"email": user.email, "password": user.password_hash}))
    return response
