from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_genre_preference import UserGenrePreference
from app.models.user_language_preference import UserLanguagePreference

from app.models.genre import Genre

def get_genre_preferences_by_user_id(user_id: int, db: Session):
  genre_preferences = (
    db.query(UserGenrePreference.genre_id, Genre.name)
    .join(Genre, UserGenrePreference.genre_id == Genre.id)
    .filter(UserGenrePreference.user_id == user_id)
    .all()
  )
  
  if not genre_preferences:
    return []
  else:
    return [name for (name,) in genre_preferences]
  
def get_language_preferences_by_user_id(user_id: int, db: Session):
  language_preferences = (
    db.query(UserLanguagePreference)
    .with_entities(UserLanguagePreference.language_code)
    .filter(UserLanguagePreference.user_id == user_id)
    .all()
  )
  
  if not language_preferences:
    return []
  else:
    return [language_code for (language_code,) in language_preferences]