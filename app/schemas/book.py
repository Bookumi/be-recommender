from pydantic import BaseModel
from typing import List
from app.schemas.genre import GenreResponse

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