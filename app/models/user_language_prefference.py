from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.book_genre import books_genres
from app.database import Base
from pydantic import Field, BaseModel

class UserLanguagePrefference(Base):
  __tablename__ = "user_language_prefferences"
  user_id = Column(Integer, unique=False, nullable=False)
  language_code = Column(String, unique=False, nullable=False)
  
  user = relationship("User", back_populates="language_prefferences")