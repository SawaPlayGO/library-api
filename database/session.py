from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL
ECHO_SQL = settings.ECHO_SQL

engine = create_engine(DATABASE_URL, echo=ECHO_SQL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Функция-зависимость для получения сессии БД.
    Используется в маршрутах через Depends.
    
    :yield: сессия SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
