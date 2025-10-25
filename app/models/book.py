from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app.models.book_genre import books_genres
from app.database import Base

class Book(Base):
  __tablename__ = "books"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=True, nullable=False)
  title = Column(String, unique=False, nullable=False)
  language_code = Column(String, unique=False, nullable=False)
  average_rating = Column(Float, unique=False, nullable=False)
  ratings_count = Column(Integer, unique=False, nullable=False)
  score = Column(Float, unique=False, nullable=False)
  url = Column(Text, unique=False, nullable=True)
  image_url = Column(Text, unique=False, nullable=True)

  genres = relationship("Genre", secondary=books_genres, back_populates="books")