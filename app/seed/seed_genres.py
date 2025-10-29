from app.database import SessionLocal
from sqlalchemy import text
import json
from pathlib import Path

def seed_genres():
    session = SessionLocal()
    file_path = Path(__file__).parent / "unique_genres.json"

    with open(file_path, "r") as f:
        genres = json.load(f)

    for name in genres:
        session.execute(
            text("""
                INSERT INTO genres (name)
                VALUES (:name)
                ON CONFLICT (name) DO NOTHING
            """),
            {"name": name}
        )

    session.commit()
    session.close()
    print("✅ Seeded genres successfully.")

if __name__ == "__main__":
    seed_genres()
