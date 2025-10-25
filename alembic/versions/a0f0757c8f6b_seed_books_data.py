"""seed books data

Revision ID: a0f0757c8f6b
Revises: b67c20769721
Create Date: 2025-10-25 13:02:07.341448

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
import json
from pathlib import Path


# revision identifiers, used by Alembic.
revision: str = 'a0f0757c8f6b'
down_revision: Union[str, Sequence[str], None] = 'b67c20769721'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Get DB session
    bind = op.get_bind()
    session = Session(bind=bind)

    # Load JSON data
    file_path = Path(__file__).parent.parent.parent / "app" / "seed" / "books_data.json"
    with open(file_path, "r") as f:
        books = json.load(f)

    # Insert records
    for b in books:
        session.execute(
            sa.text("""
                INSERT INTO books (id, title, description, language_code, average_rating, ratings_count, score, url, image_url)
                VALUES (:id, :title, :description, :language_code, :average_rating, :ratings_count, :score, :url, :image_url)
                ON CONFLICT (id) DO NOTHING
            """),
            {
                "id": b["book_id"],
                "title": b["title"],
                "description": b["description"],
                "language_code": b["language_code"],
                "average_rating": b["average_rating"],
                "ratings_count": b["ratings_count"],
                "score": b["score"],
                "url": b["url"],
                "image_url": b["image_url"]
            }
        )

    session.commit()

def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    # Load the same JSON file used in upgrade()
    file_path = Path(__file__).parent.parent.parent / "app" / "seed" / "books_data.json"
    with open(file_path, "r") as f:
        books = json.load(f)

    # Delete only those that were seeded
    book_ids = [b["book_id"] for b in books]

    session.execute(
        sa.text("DELETE FROM books WHERE id = ANY(:ids)"),
        {"ids": book_ids}
    )

    session.commit()
