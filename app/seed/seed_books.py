from pathlib import Path
import json
from sqlalchemy import text
from app.database import SessionLocal

def seed_books():
    session = SessionLocal()

    file_path = Path(__file__).parent / "books_data.json"
    if not file_path.exists():
        raise FileNotFoundError(f"Seed file not found: {file_path}")

    with open(file_path, "r") as f:
        books = json.load(f)

    print(f"Seeding {len(books)} books...")

    for b in books:
        session.execute(
            text("""
                INSERT INTO books (
                    id, title, description, language_code,
                    average_rating, ratings_count, score, url, image_url
                )
                VALUES (
                    :id, :title, :description, :language_code,
                    :average_rating, :ratings_count, :score, :url, :image_url
                )
                ON CONFLICT (id) DO NOTHING
            """),
            {
                "id": b["book_id"],
                "title": b["title"],
                "description": b.get("description"),
                "language_code": b.get("language_code"),
                "average_rating": b.get("average_rating"),
                "ratings_count": b.get("ratings_count"),
                "score": b.get("score"),
                "url": b.get("url"),
                "image_url": b.get("image_url")
            }
        )

    session.commit()
    session.close()
    print("✅ Book seeding completed successfully.")


if __name__ == "__main__":
    seed_books()
