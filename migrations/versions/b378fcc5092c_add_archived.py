"""add archived

Revision ID: b378fcc5092c
Revises: 9bc4d9d99edc
Create Date: 2024-03-27 20:39:22.239543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b378fcc5092c'
down_revision: Union[str, None] = '9bc4d9d99edc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tour_schema', sa.Column('isArchived', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tour_schema', 'isArchived')
    # ### end Alembic commands ###
