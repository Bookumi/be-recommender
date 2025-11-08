from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_genre_preference import UserGenrePreference
from app.models.user_language_preference import UserLanguagePreference
from app.schemas.user import UserGenrePreferenceRequest, UserLanguagePreferenceRequest
import traceback

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
    return [genre.name for genre in genre_preferences]
  
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
    return [language_preference.language_code for language_preference in language_preferences]


def add_genre_preferences(user_id: int, user_genre: UserGenrePreferenceRequest, db: Session):
  try:
    db.query(UserGenrePreference).filter(
      UserGenrePreference.user_id == user_id
    ).delete()
    
    if len(user_genre.genres) > 0:
      for genre_id in user_genre.genres:
        genre_preference = UserGenrePreference(
          user_id=user_id,
          genre_id=genre_id
        )
        db.add(UserGenrePreference(
          user_id=user_id,
          genre_id=genre_id
        ))
      
      db.commit()
  except Exception as e:
    db.rollback()
    print(traceback.format_exc())
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"failed to update user preferences")
  
  return user_genre

def add_language_preferences(user_id: int, user_languages: UserLanguagePreferenceRequest, db: Session):
  try:
      db.query(UserLanguagePreference).filter(
          UserLanguagePreference.user_id == user_id
      ).delete()
      valid_codes = {"en", "ind"}
      for language_code in user_languages.languages:
          if language_code not in valid_codes:
              raise ValueError(f"Invalid language code: {language_code}")
          
          db.add(UserLanguagePreference(
            user_id=user_id,
            language_code=language_code
          ))
      db.commit()
  except Exception as e:
      db.rollback()
      print(traceback.format_exc())
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=f"Failed to update user preferences, {e}"
      )
      
  return user_languages
    