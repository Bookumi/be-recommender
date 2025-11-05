from sqlalchemy.orm import Session
import app.crud.user_preference as UserGenrePrefferenceCRUD
from app.schemas.user import UserPrefferenceResponse

def get_prefferences_by_user_id(user_id: int, db: Session)->UserPrefferenceResponse:
  user_genre_prefference = UserGenrePrefferenceCRUD.get_genre_preferences_by_user_id(user_id, db)
  user_language_prefference = UserGenrePrefferenceCRUD.get_language_preferences_by_user_id(user_id, db)
  
  return UserPrefferenceResponse(
    genres=user_genre_prefference,
    languages=user_language_prefference
  )
  
  