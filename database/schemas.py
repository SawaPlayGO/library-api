from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    token: str

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str
    author: str
    year: int = Field(default=None, allow_none=True)  # type: ignore
    isbn: str = Field(default=None, allow_none=True)  # type: ignore
    copies: int

    class Config:
        from_attributes = True


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: int

    class Config:
        from_attributes = True


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: Optional[int] = None

    class Config:
        from_attributes = True


class ReaderCreate(BaseModel):
    name: str
    email: str

    class Config:
        from_attributes = True


class ReaderUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True

class BorrowCreate(BaseModel):
    reader_id: int
    book_id: int

    class Config:
        from_attributes = True


class BorrowBookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    borrow_date: str

    class Config:
        from_attributes = True