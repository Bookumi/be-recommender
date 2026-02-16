from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Query


class UserBookRatingResponse(BaseModel):
  user_id: int
  book_id: int
  rating: int
  
  class Config:
    orm_mode = True
    
class UserBookRatingFilter(BaseModel):
  user_id: Optional[int] = Field(0, description="user id")
  book_id: Optional[int] = Field(0, description="book id")
  rating: Optional[int] = Field(0, description="rating id")
  
  @classmethod
  def as_query(
    cls,
    user_id: int = Query(default_factory=int),
    book_id: int = Query(default_factory=int),
    rating: int = Query(default_factory=int),
  ):
    return cls(user_id=user_id, book_id=book_id, rating=rating)