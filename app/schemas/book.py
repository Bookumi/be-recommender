from fastapi import Query
from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.genre import GenreResponse

class GetAllBookFilter(BaseModel):
  genres: list[str] = Field(list, description="filter by its genres")
  language_code: list[str] = Field(list, description="filter by its language code")

class BookResponse(BaseModel):
  id: int
  title: str
  description: str
  language_code: str
  average_rating: float
  ratings_count: int
  score: float
  url: str
  image_url: str
  genres: List[GenreResponse]

  class Config:
    orm_mode = True

class BookFilter(BaseModel):
  genres: Optional[list[str]] = Field([], description="filter by its genres")
  language_codes: Optional[list[str]] = Field([], description="filter by its language code")
  
  @classmethod
  def as_query(cls,
               genres: list[str] = Query(default_factory=list),
               language_codes: list[str] = Query(default_factory=list)):
      return cls(genres=genres, language_codes=language_codes)
  
class SimiliarBookFilter(BaseModel):
  book_id: int = Field(..., description="book_id")
  top_k: int = Field(5, description="number of total similiar books to return")
  genres: Optional[list[str]] = Field([], description="filter by its genres")
  language_codes: Optional[list[str]] = Field([], description="filter by its language code")
  
  @classmethod
  def as_query(cls,
              book_id: int = Query(...),
              top_k: int = Query(5),
              genres: list[str] = Query(default_factory=list),
              language_codes: list[str] = Query(default_factory=list)):
      return cls(book_id=book_id, top_k=top_k, genres=genres, language_codes=language_codes)
