from sqlalchemy.orm import Session
from app.repository import genre as GenreCRUD

def get_all_genres(db: Session):
  genres = GenreCRUD.get_all_genres(db)
  
  return genres