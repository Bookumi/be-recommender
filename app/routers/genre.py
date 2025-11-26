from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.response import BaseResponse
from app.schemas.genre import GenreResponse
import app.services.genre as GenreService
from typing import List

router = APIRouter(prefix="/api/v1/genres", tags=["Genres"])

@router.get("", response_model=BaseResponse[List[GenreResponse]])
def get_all_genres(db: Session = Depends(get_db)):
  genres = GenreService.get_all_genres(db)
  
  return BaseResponse(
    message="success get all genres",
    data=genres
  )