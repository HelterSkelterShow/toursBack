"""add tour_state

Revision ID: ab5ebebf9ec8
Revises: ab68ac196800
Create Date: 2024-03-10 14:17:26.416407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab5ebebf9ec8'
down_revision: Union[str, None] = 'ab68ac196800'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tour_plan', sa.Column('state', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tour_plan', 'state')
    # ### end Alembic commands ###
