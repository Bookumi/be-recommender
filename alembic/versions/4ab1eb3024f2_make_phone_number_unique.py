"""make phone_number unique

Revision ID: 4ab1eb3024f2
Revises: e074b48d066c
Create Date: 2025-11-04 20:05:17.666797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ab1eb3024f2'
down_revision: Union[str, Sequence[str], None] = 'e074b48d066c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
	op.create_unique_constraint(
      "uq_users_phone_number",
      "users",  
      ["phone_number"]
  )

def downgrade():
  op.drop_constraint(
      "uq_users_phone_number",
      "users",
      type_="unique"
  )
