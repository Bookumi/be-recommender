from app.schemas.user_book_rating import UserBookRatingFilter
from sqlalchemy.orm import Session, joinedload
from app.models.user_book_ratings import UserBookRating
import app.repository.user_book_rating as UserBookRatingRepository

def get_user_book_rating(user_book_rating_filter: UserBookRatingFilter, db: Session):
  book = UserBookRatingRepository.get_user_book_rating(user_book_rating_filter, db)
  
  return book