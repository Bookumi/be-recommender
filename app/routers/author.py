from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.response import BaseResponse
from app.schemas.pagination import PaginatedResponse, Pagination
from app.schemas.author import AuthorResponse, AuthorFilter
from app.database import get_db
from sqlalchemy.orm import Session
import app.services.author as AuthorService


router = APIRouter(prefix="/api/v1/authors", tags=["Authors"])

@router.get("", response_model=BaseResponse[PaginatedResponse[AuthorResponse]])
def get_all_authors(
  author_filter: AuthorFilter = Depends(AuthorFilter.as_query),
  pagination: Pagination = Depends(),
  db: Session = Depends(get_db)
):
  authors, total = AuthorService.get_all_authors(author_filter, pagination, db)
  
  return BaseResponse(
    message="success get authors data",
    data=PaginatedResponse(
      total=total,
      page=pagination.page,
      limit=pagination.limit,
      items=authors
    )
  )