"""create address_id in Users Tbale

Revision ID: 01a101ace7ff
Revises: 70d94e11aca3
Create Date: 2023-11-16 12:56:49.747204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '01a101ace7ff'
down_revision: Union[str, None] = '70d94e11aca3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_fk', source_table='users', referent_table='address',
                          local_cols=['address_id'], remote_cols=["id"],
                          ondelete="CASCADE")


def downgrade():
    op.drop_constraint('address_users_fk', table_name='users',type_='foreignkey')
    op.drop_column("users", "address_id")
