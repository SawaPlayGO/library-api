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
    year: int = Field(default=None, allow_none=True) # type: ignore
    isbn: str = Field(default=None, allow_none=True) # type: ignore
    copies: int

    class Config:
        from_attributes = True

class BookResponce(BaseModel):
    title: str
    author: str
    year: int = Field(default=None, allow_none=True) # type: ignore
    isbn: str = Field(default=None, allow_none=True) # type: ignore
    copies: int

    class Config:
        from_attributes = True


class BookUpdate(BaseModel):
    title: str = Field(default=None, allow_none=True) # type: ignore
    author: str = Field(default=None, allow_none=True) # type: ignore
    year: int = Field(default=None, allow_none=True) # type: ignore
    isbn: str = Field(default=None, allow_none=True) # type: ignore
    copies: int = Field(default=None, allow_none=True) # type: ignore