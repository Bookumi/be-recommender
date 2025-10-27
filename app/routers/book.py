from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import book as BookSchema
from app.crud import book as BookCRUD

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

@router.get("", response_model=list[BookSchema.BookResponse])
def get_all_books(db: Session = Depends(get_db)):
  return BookCRUD.get_all_books(db)