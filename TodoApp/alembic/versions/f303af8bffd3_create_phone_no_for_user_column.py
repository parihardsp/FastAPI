"""Create Phone No. for User Column

Revision ID: f303af8bffd3
Revises: 
Create Date: 2023-11-16 12:40:06.287494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f303af8bffd3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users',sa.Column('Phone_number', sa.String(100), nullable=True))


def downgrade():
    op.drop_column('users', 'Phone_number')
