"""add user_language_prefference table

Revision ID: a51d09bbbc9d
Revises: 06920e1d29db
Create Date: 2025-11-05 19:36:53.629667

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a51d09bbbc9d'
down_revision: Union[str, Sequence[str], None] = '06920e1d29db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("user_language_prefferences",
    sa.Column("user_id", sa.Integer(), nullable=False),
    sa.Column("language_code", sa.String(), nullable=False),
    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("user_id", "language_code")
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user_language_prefferences")
