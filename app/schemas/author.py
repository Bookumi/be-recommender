from pydantic import BaseModel, Field
from fastapi import Query
from typing import Optional

class AuthorResponse(BaseModel):
  id: int
  name: str
  
  class Config:
      orm_mode = True

class AuthorFilter(BaseModel):
  author_name: Optional[str] = Field(..., description="author name")
  
  @classmethod
  def as_query(
    cls,
    author_name: str = Query(default_factory=str)
  ):
    return cls(author_name=author_name)