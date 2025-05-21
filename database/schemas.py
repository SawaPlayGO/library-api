from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    token: str

    model_config = {"from_attributes": True}


class BookCreate(BaseModel):
    title: str
    author: str
    year: Optional[int] = Field(default=None, json_schema_extra={"nullable": True})
    isbn: Optional[str] = Field(default=None, json_schema_extra={"nullable": True})
    copies: int

    model_config = {"from_attributes": True}


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: int

    model_config = {"from_attributes": True}


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: Optional[int] = None

    model_config = {"from_attributes": True}


class ReaderCreate(BaseModel):
    name: str
    email: str

    model_config = {"from_attributes": True}


class ReaderUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

    model_config = {"from_attributes": True}


class BorrowCreate(BaseModel):
    reader_id: int
    book_id: int

    model_config = {"from_attributes": True}


class BorrowBookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    borrow_date: str

    model_config = {"from_attributes": True}

