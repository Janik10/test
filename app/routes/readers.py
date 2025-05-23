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

@router.post("/", response_model=schemas.Reader)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_reader = models.Reader(**reader.dict())
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader

@router.get("/", response_model=list[schemas.Reader])
def read_readers(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Reader).all()

@router.get("/{reader_id}/borrowed", response_model=list[schemas.Book])
def get_borrowed_books(reader_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    borrows = db.query(models.BorrowedBook).filter(
        models.BorrowedBook.reader_id == reader_id,
        models.BorrowedBook.return_date == None
    ).all()
    book_ids = [b.book_id for b in borrows]
    return db.query(models.Book).filter(models.Book.id.in_(book_ids)).all()
