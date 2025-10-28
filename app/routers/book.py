from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import book as BookSchema
from app.schemas import pagination as PaginationSchema
from app.crud import book as BookCRUD

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

@router.get("", response_model=PaginationSchema.PaginatedResponse[BookSchema.BookResponse])
def get_all_books(
  book_filter: BookSchema.BookFilter = Depends(BookSchema.BookFilter.as_query),
  pagination: PaginationSchema.Pagination = Depends(),
  db: Session = Depends(get_db)
):
  books, total = BookCRUD.get_all_books(db, pagination, book_filter)
  return PaginationSchema.PaginatedResponse(
    total=total,
    page=pagination.page,
    limit=pagination.limit,
    items=books
  )

@router.get("/{id}", response_model=BookSchema.BookResponse)
def get_detail_book(id: int, db: Session = Depends(get_db)):
  book = BookCRUD.get_detail_book(db, id)

  if not book:
    raise HTTPException(status_code=404, detail="book not found")

  return book