from app.schemas.user_book_rating import UserBookRatingFilter
from sqlalchemy.orm import Session
from app.models.user_book_ratings import UserBookRating

def get_user_book_rating(user_book_rating_filter: UserBookRatingFilter, db: Session):
  books = (
    db
    .query(UserBookRating)
    .filter(UserBookRating.book_id.__eq__(user_book_rating_filter.book_id))
    .filter(UserBookRating.user_id.__eq__(user_book_rating_filter.user_id))
    .first()
  )
  
  return books