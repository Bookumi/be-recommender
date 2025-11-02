from sqlalchemy.orm import Session, joinedload
from app.models.book import Book
from app.models.genre import Genre
from app.schemas.pagination import Pagination
from app.schemas.book import BookFilter, SimiliarBookFilter, GetCFSVDRecommendation
from typing import Union, Any

def get_all_books(book_filter: BookFilter, pagination: Pagination, db: Session):
  query = db.query(Book).options(joinedload(Book.genres)).order_by(Book.score.desc())

  if len(book_filter.language_codes) != 0:
    query = query.filter(Book.language_code.in_(book_filter.language_codes))

  if len(book_filter.genres) != 0:
    query = query.join(Book.genres).filter(Genre.name.in_(book_filter.genres))

  books = (
    query
    .offset(pagination.skip)
    .limit(pagination.limit)
    .all()
  )
  total = query.count()

  return books, total

def get_detail_book(id: int, db: Session):
  book = db.query(Book).filter(Book.id == id).first()

  return book

def get_similiar_books(
  book_filter: Union[SimiliarBookFilter, GetCFSVDRecommendation, Any],
  pagination: Pagination,
  ids: list[int],
  db: Session
):
  query = db.query(Book).options(joinedload(Book.genres)).filter(Book.id.in_(ids))

  if isinstance(book_filter, SimiliarBookFilter):
    if len(book_filter.language_codes) != 0:
      query = query.filter(Book.language_code.in_(book_filter.language_codes))

    if len(book_filter.genres) != 0:
      query = query.join(Book.genres).filter(Genre.name.in_(book_filter.genres))

  books = (
    query
    .offset(pagination.skip)
    .limit(pagination.limit)
    .all()
  )
  total = query.count()

  return books, total