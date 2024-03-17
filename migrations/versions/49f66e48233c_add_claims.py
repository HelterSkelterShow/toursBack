"""add claims

Revision ID: 49f66e48233c
Revises: 6f8ab28ef5fa
Create Date: 2024-03-17 14:12:11.305536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49f66e48233c'
down_revision: Union[str, None] = '6f8ab28ef5fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('claims',
    sa.Column('claimId', sa.UUID(), nullable=False),
    sa.Column('touristId', sa.Integer(), nullable=True),
    sa.Column('gidEmail', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('publicTourId', sa.UUID(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('creationDateTime', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['publicTourId'], ['tour_plan.id'], ),
    sa.ForeignKeyConstraint(['touristId'], ['user.id'], ),
    sa.PrimaryKeyConstraint('claimId')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('claims')
    # ### end Alembic commands ###