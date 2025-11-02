from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import BookFilter, BookResponse, SimiliarBookFilter, GetCFSVDRecommendation
from app.schemas.pagination import PaginatedResponse, Pagination
from app.schemas.response import BaseResponse
from app.crud import book as BookCRUD
import app.recommenders.faiss as FAISSRecommender
import app.recommenders.cf_svd as SVDRecommender
import app.services.book as BookService

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

@router.get("", response_model=BaseResponse[PaginatedResponse[BookResponse]])
def get_all_books(
  book_filter: BookFilter = Depends(BookFilter.as_query),
  pagination: Pagination = Depends(),
  db: Session = Depends(get_db)
):
  books, total = BookService.get_all_books(book_filter, pagination, db)
  
  return BaseResponse(
    message="success get all books",
    data=PaginatedResponse(
      total=total,
      page=pagination.page,
      limit=pagination.limit,
      items=books
    )
  )

@router.get("/similiar", response_model=BaseResponse[PaginatedResponse[BookResponse]])
def get_similiar_books(
  book_filter: SimiliarBookFilter = Depends(SimiliarBookFilter.as_query),
  pagination: Pagination = Depends(),
  db: Session = Depends(get_db)
):
  books, total = BookService.get_similiar_books(
    book_filter,
    pagination,
    db,
  )

  return BaseResponse(
    message=f"success get similiar books of book_id {book_filter.book_id}",
    data=PaginatedResponse(
      total=total,
      page=pagination.page,
      limit=pagination.limit,
      items=books
    )
  )

@router.get("/{id}", response_model=BaseResponse[BookResponse])
def get_detail_book(id: int, db: Session = Depends(get_db)):
  book = BookService.get_detail_book(id, db)

  if not book:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")

  return BaseResponse(
    message="success get detail book",
    data=book
  )

@router.get("/similiar/cf-svd", response_model=BaseResponse[PaginatedResponse[BookResponse]])
def get_cf_svd_recommendation(
  get_recommendation_request: GetCFSVDRecommendation = Depends(GetCFSVDRecommendation.as_query),
  pagination: Pagination = Depends(),
  db: Session = Depends(get_db)
):
  
  books, total = BookService.get_cf_svd_recommendation(get_recommendation_request, pagination, db)

  return BaseResponse(
  	message=f"success get recommended books for user with id {get_recommendation_request.user_id}",
  	data=PaginatedResponse(
  	  total=total,
  	  page=pagination.page,
  	  limit=pagination.limit,
  	  items=books
  	)
  )