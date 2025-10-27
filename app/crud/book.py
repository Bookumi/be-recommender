from sqlalchemy.orm import Session, joinedload
from app.models.book import Book
from app.models.pagination import Pagination

def get_all_books(db: Session, pagination: Pagination):
  query = db.query(Book).options(joinedload(Book.genres)).order_by(Book.score.desc())
  books = (
    query
    .offset(pagination.skip)
    .limit(pagination.limit)
    .all()
  )
  total = query.count()

  return books, total