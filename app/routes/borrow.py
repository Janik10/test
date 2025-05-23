from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime
from .. import models, schemas
from ..database import SessionLocal
from ..utils import SECRET_KEY, ALGORITHM

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Недействительный токен")

@router.post("/take")
def borrow_book(data: schemas.BorrowRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == data.book_id).first()
    if not book or book.quantity < 1:
        raise HTTPException(status_code=400, detail="Книга недоступна")

    count = db.query(models.BorrowedBook).filter(
        models.BorrowedBook.reader_id == data.reader_id,
        models.BorrowedBook.return_date == None
    ).count()

    if count >= 3:
        raise HTTPException(status_code=400, detail="У читателя уже 3 книги")

    book.quantity -= 1
    borrow = models.BorrowedBook(book_id=data.book_id, reader_id=data.reader_id)
    db.add(borrow)
    db.commit()
    return {"message": "Книга выдана"}

@router.post("/return")
def return_book(data: schemas.ReturnRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    borrow = db.query(models.BorrowedBook).filter(
        models.BorrowedBook.book_id == data.book_id,
        models.BorrowedBook.reader_id == data.reader_id,
        models.BorrowedBook.return_date == None
    ).first()

    if not borrow:
        raise HTTPException(status_code=400, detail="Нет записи о выдаче")

    book = db.query(models.Book).filter(models.Book.id == data.book_id).first()
    book.quantity += 1
    borrow.return_date = datetime.utcnow()
    db.commit()
    return {"message": "Книга возвращена"}
