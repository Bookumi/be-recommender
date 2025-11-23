from pathlib import Path
import json
from sqlalchemy import text
from app.database import SessionLocal

def seed_authors():
    session = SessionLocal()

    file_path = Path(__file__).parent / "authors_data.json"
    if not file_path.exists():
        raise FileNotFoundError(f"Seed file not found: {file_path}")

    with open(file_path, "r") as f:
        authors = json.load(f)

    print(f"Seeding {len(authors)} author...")

    for b in authors:
        session.execute(
            text("""
                INSERT INTO authors (
                    id, name, total_rating, score, average_rating
                )
                VALUES (
                    :id, :name, :total_rating, :score, :average_rating
                )
                ON CONFLICT (id) DO NOTHING
            """),
            {
                "id": b["author_id"],
                "name": b["author_name"],
                "total_rating": b["author_ratings_count"],
                "score": b["author_score"],
                "average_rating": b["author_avg_rating"],
            }
        )

    session.commit()
    session.close()
    print("✅ Author seeding completed successfully.")


if __name__ == "__main__":
    seed_authors()
