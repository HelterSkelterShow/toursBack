"""refactor claims table

Revision ID: e02eca060497
Revises: bb35efa8a272
Create Date: 2024-03-17 22:15:43.529942

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e02eca060497'
down_revision: Union[str, None] = 'bb35efa8a272'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('claim', sa.Column('type', sa.String(), nullable=True))
    op.alter_column('claim', 'gidEmail',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('claim', 'gidEmail',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('claim', 'type')
    # ### end Alembic commands ###
