"""add apt no. in address table

Revision ID: 6c1263409646
Revises: 01a101ace7ff
Create Date: 2023-11-16 16:27:28.855986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c1263409646'
down_revision: Union[str, None] = '01a101ace7ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('address',
                  sa.Column('apt_number', sa.String(100), nullable=True ))


def downgrade() -> None:
    op.drop_column('address','apt_number')
