from pathlib import Path
import json
from sqlalchemy import text
from app.database import SessionLocal

def seed_authors_books():
    session = SessionLocal()

    file_path = Path(__file__).parent / "authors_data.json"
    if not file_path.exists():
        raise FileNotFoundError(f"Seed file not found: {file_path}")

    with open(file_path, "r") as f:
        authors = json.load(f)

    print(f"Seeding {len(authors)} authors books...")

    for b in authors:
        session.execute(
            text("""
                INSERT INTO authors_books (
                    author_id, book_id
                )
                VALUES (
                    :author_id, :book_id
                )
                ON CONFLICT DO NOTHING
            """),
            {
                "author_id": b["author_id"],
                "book_id": b["book_id"],
            }
        )

    session.commit()
    session.close()
    print("✅ Author Books seeding completed successfully.")


if __name__ == "__main__":
    seed_authors_books()
