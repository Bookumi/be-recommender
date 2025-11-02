from pathlib import Path
import json
from sqlalchemy import text
from app.database import SessionLocal

def seed_user_book_ratings():
  session = SessionLocal()
  
  file_path = Path(__file__).parent / "svd_interactions.json"
  if not file_path.exists():
    raise FileNotFoundError(f"seed file not found: {file_path}")
  
  with open(file_path, "r") as f:
    user_book_ratings = json.load(f)

  for u in user_book_ratings:
    session.execute(
      text("""
          INSERT INTO user_book_ratings (
            user_id, book_id, rating
          )
          VALUES (
            :user_id, :book_id, :rating
          )
           """
      ),
      {
        "user_id": u["user_id"],
        "book_id": u["book_id"],
        "rating": u["rating"]
      }
    )
    
  session.commit()
  session.close()
  print("✅ User book rating seeding completed successfully.")
  
if __name__ == "__main__":
    seed_user_book_ratings()
