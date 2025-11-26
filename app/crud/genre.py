
from sqlalchemy.orm import Session
from app.models.genre import Genre

def get_all_genres(db: Session):
  genres = db.query(Genre).all()
  
  return genres