from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import book as BookSchema
from app.schemas import pagination as PaginationSchema
from app.models import pagination as PaginationModel
from app.crud import book as BookCRUD

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

@router.get("", response_model=PaginationSchema.PaginatedResponse[BookSchema.BookResponse])
def get_all_books(
  pagination: PaginationModel.Pagination = Depends(),
  db: Session = Depends(get_db)
):
  books, total = BookCRUD.get_all_books(db, pagination)
  return PaginationSchema.PaginatedResponse(
    total=total,
    page=pagination.page,
    limit=pagination.limit,
    items=books
  )