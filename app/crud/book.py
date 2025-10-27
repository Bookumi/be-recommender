from sqlalchemy.orm import Session
from app.models.book import Book

def get_all_books(db: Session):
  return db.query(Book).order_by(Book.score.desc())