from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import BookFilter, BookResponse, SimiliarBookFilter, GetCFSVDRecommendation, AddRating, BookTitles, BookTitleFilter
from app.schemas.pagination import PaginatedResponse, Pagination
from app.schemas.response import BaseResponse
import app.services.book as BookService
from app.middlewares.auth import verify_auth_token
from app.schemas.auth import JWTPayload

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

@router.get("/titles", response_model=BaseResponse[PaginatedResponse[BookTitles]])
def get_all_book_titles(
  book_title_filter: BookTitleFilter = Depends(BookTitleFilter.as_query),
  pagination: Pagination = Depends(),
  db: Session = Depends(get_db)
):
  book_title, total = BookService.get_book_titles(book_title_filter, pagination, db)
  
  return BaseResponse(
    message="success get book title data",
    data=PaginatedResponse(
      total=total,
      page=pagination.page,
      limit=pagination.limit,
      items=book_title,
    )
  )

@router.post("/rating", response_model=BaseResponse[AddRating])
def add_rating(
  add_rating_request: AddRating,
  db: Session = Depends(get_db),
  current_user: JWTPayload = Depends(verify_auth_token)
):
  add_rating_payload = add_rating_request.model_copy(update={"user_id": current_user.sub})
  
  if int(add_rating_payload.rating) < 1 or int(add_rating_payload.rating) > 5:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="rating rabge must greater than 0 and less than or equal to 5 (1 - 5)"
    )
  
  book_rating = BookService.add_rating(add_rating_payload, db)
  
  return BaseResponse(
    message="success add or update book rating",
    data=book_rating
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
  pagination: Pagination = Depends(),
  db: Session = Depends(get_db),
  current_user: JWTPayload = Depends(verify_auth_token)
):
  request_with_user: GetCFSVDRecommendation = {
    "user_id": current_user.sub,
    "liked_books": []
  }
  
  books, total = BookService.get_cf_svd_recommendation(request_with_user, pagination, db)

  return BaseResponse(
  	message=f"success get recommended books for user with id {current_user.sub}",
  	data=PaginatedResponse(
  	  total=total,
  	  page=pagination.page,
  	  limit=pagination.limit,
  	  items=books
  	)
  )