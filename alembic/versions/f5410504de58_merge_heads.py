"""merge heads

Revision ID: f5410504de58
Revises: 4172bdb04b21, a0f0757c8f6b
Create Date: 2025-10-25 13:55:01.458120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5410504de58'
down_revision: Union[str, Sequence[str], None] = ('4172bdb04b21', 'a0f0757c8f6b')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
