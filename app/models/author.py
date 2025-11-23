from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.authors_books import authors_books
from app.database import Base
from pydantic import Field, BaseModel
from app.models.user_book_ratings import UserBookRating


class Book(Base):
  __tablename__ = "authors"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=False, nullable=False)
  total_rating = Column(Integer, unique=False, nullable=True)
  score = Column(Float, unique=False, nullable=True)
  average_rating = Column(Float, unique=False, nullable=False)

  books = relationship("Book", secondary=authors_books, back_populates="books")

