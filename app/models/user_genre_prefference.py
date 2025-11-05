from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.book_genre import books_genres
from app.database import Base
from pydantic import Field, BaseModel

class UserGenrePrefference(Base):
  __tablename__ = "user_book_ratings"
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
  genre_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
  
  user = relationship("User", back_populates="genre_prefferences")
  genre = relationship("Genre", back_populates="genre_prefferences")