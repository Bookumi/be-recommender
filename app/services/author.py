from sqlalchemy.orm import Session
from app.schemas.author import AuthorFilter
from app.schemas.pagination import Pagination
from app.repository import author as AuthorRepository

def get_all_authors(
  author_filter: AuthorFilter,
  pagination: Pagination,
  db: Session
):
  authors, total = AuthorRepository.get_all_authors(author_filter, pagination, db)
  
  return authors, total