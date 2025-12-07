from fastapi import Query
from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.genre import GenreResponse
from app.schemas.author import AuthorResponse

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
  authors: List[AuthorResponse]

  class Config:
    orm_mode = True

class BookFilter(BaseModel):
  title: Optional[str] = Field(..., description="filter by book title")
  genres: Optional[list[str]] = Field([], description="filter by its genres")
  language_codes: Optional[list[str]] = Field([], description="filter by its language code")
  authors: Optional[list[str]] = Field([], description="filter by its authors")
  
  @classmethod
  def as_query(
    cls,
    title: str = Query(default_factory=str),
    genres: list[str] = Query(default_factory=list),
    language_codes: list[str] = Query(default_factory=list),
    authors: list[str] = Query(default_factory=list)
  ):
    return cls(title=title, genres=genres, language_codes=language_codes, authors=authors)
  
class SimiliarBookFilter(BaseModel):
  book_id: int = Field(..., description="book_id")
  book_language_code: str = Field(..., description="book language code")
  top_k: int = Field(5, description="number of total similiar books to return")
  genres: Optional[list[str]] = Field([], description="filter by its genres")
  language_codes: Optional[list[str]] = Field([], description="filter by its language code")
  
  @classmethod
  def as_query(
    cls,
    book_id: int = Query(...),
    book_language_code: str = Query(...),
    top_k: int = Query(5),
    genres: list[str] = Query(default_factory=list),
    language_codes: list[str] = Query(default_factory=list)
  ):
    return cls(book_id=book_id, book_language_code=book_language_code, top_k=top_k, genres=genres, language_codes=language_codes)

class GetCFSVDRecommendation(BaseModel):
  user_id:  Optional[int] = Field(None, description="user_id")
  liked_books: Optional[list[int]] = Query(default=[])
  
class AddRating(BaseModel):
  rating: int
  _user_id: Optional[int]
  book_id: int
  
class BookTitles(BaseModel):
  id: int
  title: str

class BookTitleFilter(BaseModel):
  title: Optional[str] = Field(..., description="book title")
  
  @classmethod
  def as_query(
    cls,
    title: str = Query(default_factory=str)
  ):
    return cls(title=title)