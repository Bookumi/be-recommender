from sqlalchemy.orm import Session, joinedload
from app.models.book import Book
from app.models.genre import Genre
from app.schemas.pagination import Pagination
from app.schemas.book import BookFilter

def get_all_books(db: Session, pagination: Pagination, book_filter: BookFilter):
  query = db.query(Book).options(joinedload(Book.genres)).order_by(Book.score.desc())

  print(book_filter, pagination)

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