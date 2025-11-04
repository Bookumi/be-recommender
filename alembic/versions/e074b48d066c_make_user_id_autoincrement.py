"""make user id autoincrement

Revision ID: e074b48d066c
Revises: 3678d0da3c4e
Create Date: 2025-11-04 16:24:18.067189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'e074b48d066c'
down_revision: Union[str, Sequence[str], None] = '3678d0da3c4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    connection = op.get_bind()
    
    # Create sequence for BIGINT
    op.execute('CREATE SEQUENCE IF NOT EXISTS users_id_seq')
    
    # Set the sequence to current max id + 1
    result = connection.execute(text("SELECT COALESCE(MAX(id), 0) FROM users"))
    max_id = result.scalar()
    op.execute(text(f"SELECT setval('users_id_seq', {max_id + 1}, false)"))
    
    # Change column type to BIGINT and set default to use sequence
    op.alter_column('users', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.BIGINT(),
               server_default=text("nextval('users_id_seq'::regclass)"),
               existing_nullable=False,
               postgresql_using="id::bigint")


def downgrade() -> None:
    """Downgrade schema."""
    connection = op.get_bind()
    
    # Remove default value first
    op.alter_column('users', 'id',
               existing_type=sa.BIGINT(),
               server_default=None,
               existing_nullable=False)
    
    # Change back to INTEGER
    op.alter_column('users', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               postgresql_using="id::integer")
    
    # Drop sequence
    op.execute('DROP SEQUENCE IF EXISTS users_id_seq')