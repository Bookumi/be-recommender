"""seed genre data

Revision ID: ad978442f879
Revises: f5410504de58
Create Date: 2025-10-25 13:55:36.529697

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
import json
from pathlib import Path


# revision identifiers, used by Alembic.
revision: str = 'ad978442f879'
down_revision: Union[str, Sequence[str], None] = 'f5410504de58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    file_path = Path(__file__).parent.parent.parent / "app" / "seed" / "unique_genres.json"
    with open(file_path, "r") as f:
        genres = json.load(f)

    for name in genres:
        session.execute(
            sa.text("""
                INSERT INTO genres (name)
                VALUES (:name)
                ON CONFLICT (name) DO NOTHING
            """),
            {"name": name}
        )

    session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    file_path = Path(__file__).parent.parent.parent / "app" / "seed" / "unique_genres.json"
    with open(file_path, "r") as f:
        genres = json.load(f)

    session.execute(
        sa.text("DELETE FROM genres WHERE name = ANY(:names)"),
        {"names": genres}
    )

    session.commit()
