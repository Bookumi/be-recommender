"""seed book_genre data

Revision ID: 4f379d49744b
Revises: ad978442f879
Create Date: 2025-10-25 14:12:43.912745

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
import json
from pathlib import Path


# revision identifiers, used by Alembic.
revision: str = '4f379d49744b'
down_revision: Union[str, Sequence[str], None] = 'ad978442f879'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    # Load JSON file
    file_path = Path(__file__).parent.parent.parent / "app" / "seed" / "book_genres.json"
    with open(file_path, "r") as f:
        data = json.load(f)

    # Loop through each book and its genres
    for book_id, genres in data.items():
        for genre_name in genres:
            # Get genre_id
            result = session.execute(
                sa.text("SELECT id FROM genres WHERE name = :name"),
                {"name": genre_name}
            ).fetchone()

            if not result:
                # Skip if genre not found (or optionally insert)
                continue

            genre_id = result[0]

            # Insert relationship if not exists
            session.execute(
                sa.text("""
                    INSERT INTO books_genres (book_id, genre_id)
                    VALUES (:book_id, :genre_id)
                    ON CONFLICT DO NOTHING
                """),
                {"book_id": int(book_id), "genre_id": genre_id}
            )

    session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    # Load JSON file again to know what to delete
    file_path = Path(__file__).parent.parent.parent / "app" / "seed" / "book_genres.json"
    with open(file_path, "r") as f:
        data = json.load(f)

    # Gather all book IDs
    book_ids = [int(book_id) for book_id in data.keys()]

    # Delete only those seeded relations
    session.execute(
        sa.text("DELETE FROM books_genres WHERE book_id = ANY(:ids)"),
        {"ids": book_ids}
    )

    session.commit()