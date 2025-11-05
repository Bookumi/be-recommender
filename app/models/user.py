from sqlalchemy import Column, UUID, Integer, String, Float, Text
from app.database import Base
from sqlalchemy.orm import relationship
from app.models.user_book_ratings import UserBookRating  
from app.models.user_genre_preference import UserGenrePreference
from app.models.user_language_preference import UserLanguagePreference

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  name = Column(String(50), unique=False, nullable=False)
  email = Column(String(50), unique=True, nullable=False)
  phone_number = Column(String(20), unique=True, nullable=True)
  password = Column(Text(), unique=True, nullable=False)
  
  book_ratings = relationship(UserBookRating, back_populates="user")
  genre_preferences = relationship(UserGenrePreference, back_populates="user")
  language_preferences = relationship(UserLanguagePreference, back_populates="user")
