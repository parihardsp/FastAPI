"""Create New Table- Address

Revision ID: 70d94e11aca3
Revises: f303af8bffd3
Create Date: 2023-11-16 12:48:01.848231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70d94e11aca3'
down_revision: Union[str, None] = 'f303af8bffd3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('address',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key =True),
                    sa.Column('address1', sa.String(100), nullable=False),
                    sa.Column('address2', sa.String(100), nullable=False),
                    sa.Column('city',sa.String(100), nullable=False),
                    sa.Column('state', sa.String(100), nullable=False),
                    sa.Column('postalcode', sa.String(100), nullable=False),
                    sa.Column('country', sa.String(100), nullable=False)
                    )


def downgrade():
    op.drop_table("address")
