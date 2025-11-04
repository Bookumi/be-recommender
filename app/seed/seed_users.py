from pathlib import Path
import json
from sqlalchemy import text
from app.database import SessionLocal
from faker import Faker
from app.utils.authentication import hash_password

def seed_users():
  session = SessionLocal()
  
  file_path = Path(__file__).parent / "svd_interactions.json"
  if not file_path.exists():
    raise FileNotFoundError(f"seed file not found: {file_path}")
  
  with open(file_path, "r") as f:
    users = json.load(f)
  
  
  feker_instance = Faker()
  
  # This default password is just for development purpose
  # Please use proper password in production
  hashed_default_password = hash_password("User#123")
    
  for u in users:
    session.execute(
      text("""
          INSERT INTO users (
            id, name, email, phone_number, password
          )
          VALUES (
            :id, :name, :email, :phone_number, :password
          )
          ON CONFLICT (id) DO NOTHING
           """
      ),
      {
        "id": u["user_id"],
        "name": feker_instance.name(),
        "email": feker_instance.email(domain="gmail.com"),
        "phone_number": feker_instance.phone_number(),
        "password": hashed_default_password,
      }
    )
    
  session.commit()
  session.close()
  print("✅ User seeding completed successfully.")
  
if __name__ == "__main__":
    seed_users()
