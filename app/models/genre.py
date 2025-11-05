from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.book_genre import books_genres
from app.models.user_genre_preference import UserGenrePreference

class Genre(Base):
  __tablename__ = "genres"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=True, nullable=False)
  
  books = relationship("Book", secondary=books_genres, back_populates="genres")
  user_preferences = relationship(UserGenrePreference, back_populates="genre")