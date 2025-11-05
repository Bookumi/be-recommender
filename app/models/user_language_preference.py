from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.book_genre import books_genres
from app.database import Base
from pydantic import Field, BaseModel

class UserLanguagePreference(Base):
  __tablename__ = "user_language_preferences"
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
  language_code = Column(String, unique=False, nullable=False)
  
  user = relationship("User", back_populates="language_preferences")