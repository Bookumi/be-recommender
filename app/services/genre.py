from sqlalchemy.orm import Session
from app.crud import genre as GenreCRUD

def get_all_genres(db: Session):
  genres = GenreCRUD.get_all_genres(db)
  
  return genres