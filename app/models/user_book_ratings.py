from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.book_genre import books_genres
from app.database import Base
from pydantic import Field, BaseModel

class UserBookRating(Base):
  __tablename__ = "user_book_ratings"
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
  book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
  rating = Column(Integer, nullable=False)
  
  user = relationship("User", back_populates="book_ratings")
  book = relationship("Book", back_populates="book_ratings")