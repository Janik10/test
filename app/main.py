from fastapi import FastAPI
from .database import Base, engine
from .routes import auth, books, readers, borrow

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library System")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(readers.router, prefix="/readers", tags=["Readers"])
app.include_router(borrow.router, prefix="/borrow", tags=["Borrow"])
