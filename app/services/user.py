from sqlalchemy.orm import Session
import app.crud.user_preference as UserGenrePrefferenceCRUD
from app.schemas.user import UserPreferenceResponse, UserGenrePreferenceRequest, UserLanguagePreferenceRequest, UserPreferenceRequest

def get_preferences_by_user_id(user_id: int, db: Session)->UserGenrePrefferenceCRUD:
  user_genre_prefference = UserGenrePrefferenceCRUD.get_genre_preferences_by_user_id(user_id, db)
  user_language_prefference = UserGenrePrefferenceCRUD.get_language_preferences_by_user_id(user_id, db)
  
  return UserPreferenceResponse(
    user_id=user_id,
    genres=user_genre_prefference,
    languages=user_language_prefference
  )
  
def add_user_preferences(user_id: int, request_payload: UserPreferenceRequest, db: Session):
  _ = UserGenrePrefferenceCRUD.add_genre_preferences(user_id, request_payload, db)
  _ = UserGenrePrefferenceCRUD.add_language_preferences(user_id, request_payload, db)
  
  updated_preference = get_preferences_by_user_id(user_id, db)
  
  return updated_preference