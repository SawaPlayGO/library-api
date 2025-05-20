from fastapi import APIRouter, Depends, HTTPException, Request
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database.session import get_db
from database.models import User
from database.schemas import UserCreate, TokenResponse
from utils.jwt import jwt_handler
from utils.rate_limiter import limiter
from config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
@limiter.limit(f"{settings.RATE_LIMITER}/minute")
def register(request: Request, register_user: UserCreate, db: Session = Depends(get_db)) -> TokenResponse:
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
    response = TokenResponse(token=jwt_handler.generate_token({"email": user.email, "password": user.password_hash}))
    return response


@router.post("/login", response_model=TokenResponse)
@limiter.limit(f"{settings.RATE_LIMITER}/minute")
def login(request: Request, login_user: UserCreate, db: Session = Depends(get_db)) -> TokenResponse:
    """
    Обрабатывает вход пользователя.

    Проверяет учетные данные пользователя на основе предоставленных данных входа.

    Аргументы:
        login_user (UserCreate): Данные входа пользователя.
        db (Session): Сессия базы данных. По умолчанию Depends(get_db).

    Возвращает:
        User: Информация о пользователе.

    Вызывает исключение:
        HTTPException: Если предоставленная электронная почта не существует.
    """
    user = db.query(User).filter(User.email == login_user.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(secret=login_user.password, hash=str(user.password_hash)):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    response = TokenResponse(token=jwt_handler.generate_token({"email": user.email, "password": user.password_hash}))
    return response