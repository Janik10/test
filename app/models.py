from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)
    isbn = Column(String, unique=True)
    quantity = Column(Integer, default=1)
    description = Column(String)

class Reader(Base):
    __tablename__ = "readers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class BorrowedBook(Base):
    __tablename__ = "borrowed_books"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    reader_id = Column(Integer, ForeignKey("readers.id"))
    borrow_date = Column(DateTime(timezone=True), server_default=func.now())
    return_date = Column(DateTime(timezone=True), nullable=True)
