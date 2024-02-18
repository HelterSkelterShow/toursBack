"""add name

Revision ID: fe6ff402ef2f
Revises: f7b180d22d91
Create Date: 2024-02-04 23:36:18.014400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe6ff402ef2f'
down_revision: Union[str, None] = 'f7b180d22d91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'name')
    # ### end Alembic commands ###
