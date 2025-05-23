from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    quantity: int = 1
    description: Optional[str] = None

class BookCreate(BookBase): pass

class Book(BookBase):
    id: int
    class Config:
        orm_mode = True

class ReaderBase(BaseModel):
    name: str
    email: EmailStr

class ReaderCreate(ReaderBase): pass

class Reader(ReaderBase):
    id: int
    class Config:
        orm_mode = True

class BorrowRequest(BaseModel):
    book_id: int
    reader_id: int

class ReturnRequest(BaseModel):
    book_id: int
    reader_id: int
