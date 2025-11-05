from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_genre_prefference import UserGenrePrefference
from app.models.genre import Genre

def get_prefferences_by_user_id(user_id: int, db: Session):
  user_prefference = (
    db.query(UserGenrePrefference.genre_id, Genre.name)
    .join(Genre, UserGenrePrefference.genre_id == Genre.id)
    .filter(UserGenrePrefference.user_id == user_id)
    .all()
  )
  
  if not user_prefference:
    return []
  else:
    return [name for (name,) in user_prefference]