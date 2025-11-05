"""add user_genre_prefference table

Revision ID: 06920e1d29db
Revises: 4ab1eb3024f2
Create Date: 2025-11-05 13:02:42.907415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06920e1d29db'
down_revision: Union[str, Sequence[str], None] = '4ab1eb3024f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("user_genre_preferences",
    sa.Column("user_id", sa.Integer(), nullable=False),
    sa.Column("genre_id", sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["genre_id"], ["genres.id"], ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("user_id", "genre_id")
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user_genre_preferences")
