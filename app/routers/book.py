from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import BookFilter, BookResponse
from app.schemas.pagination import PaginatedResponse, Pagination
from app.schemas.response import BaseResponse
from app.crud import book as BookCRUD

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

@router.get("", response_model=BaseResponse[PaginatedResponse[BookResponse]])
def get_all_books(
  book_filter: BookFilter = Depends(BookFilter.as_query),
  pagination: Pagination = Depends(),
  db: Session = Depends(get_db)
):
  books, total = BookCRUD.get_all_books(db, pagination, book_filter)
  return BaseResponse(
    message="success get all books",
    data=PaginatedResponse(
      total=total,
      page=pagination.page,
      limit=pagination.limit,
      items=books
    )
  )

@router.get("/{id}", response_model=BaseResponse[BookResponse])
def get_detail_book(id: int, db: Session = Depends(get_db)):
  book = BookCRUD.get_detail_book(db, id)

  if not book:
    raise HTTPException(status_code=404, detail="book not found")

  return BaseResponse(
    message="success get detail book",
    data=book
  )