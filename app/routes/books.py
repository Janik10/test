from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
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

@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/", response_model=list[schemas.Book])
def read_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, updated: schemas.BookCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    for key, value in updated.dict().items():
        setattr(book, key, value)
    db.commit()
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    db.delete(book)
    db.commit()
    return {"message": "Книга удалена"}
