from pathlib import Path
import json
from sqlalchemy import text
from app.database import SessionLocal

def seed_book_genres():
    session = SessionLocal()

    file_path = Path(__file__).parent / "book_genres.json"
    if not file_path.exists():
        raise FileNotFoundError(f"Seed file not found: {file_path}")

    with open(file_path, "r") as f:
        data = json.load(f)

    print(f"Seeding book-genre relationships for {len(data)} books...")

    inserted = 0
    skipped = 0

    for book_id, genres in data.items():
        for genre_name in genres:
            # Find genre_id
            result = session.execute(
                text("SELECT id FROM genres WHERE name = :name"),
                {"name": genre_name}
            ).fetchone()

            if not result:
                skipped += 1
                continue

            genre_id = result[0]

            # Insert relationship (ignore if already exists)
            session.execute(
                text("""
                    INSERT INTO books_genres (book_id, genre_id)
                    VALUES (:book_id, :genre_id)
                    ON CONFLICT DO NOTHING
                """),
                {"book_id": int(book_id), "genre_id": genre_id}
            )

            inserted += 1

    session.commit()
    session.close()

    print(f"✅ Done seeding book-genre relations.")
    print(f"Inserted: {inserted} | Skipped (genre not found): {skipped}")


if __name__ == "__main__":
    seed_book_genres()
