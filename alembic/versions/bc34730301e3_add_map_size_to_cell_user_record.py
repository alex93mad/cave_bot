"""add map_size to cell, user_record

Revision ID: bc34730301e3
Revises: 
Create Date: 2024-05-14 23:43:41.840729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'bc34730301e3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cell_13_05_2024', sa.Column('map', sa.Integer(), nullable=False, server_default = "20"))
    op.add_column('user_record_13_05_2024', sa.Column('map', sa.Integer(), nullable=False, server_default = "20"))
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_record_13_05_2024', 'map')
    op.drop_column('cell_13_05_2024', 'map')
    # ### end Alembic commands ###