"""add creatorTours tables

Revision ID: 5b1dbc1de0b3
Revises: fe6ff402ef2f
Create Date: 2024-02-10 16:43:47.670366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b1dbc1de0b3'
down_revision: Union[str, None] = 'fe6ff402ef2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tour_schema',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('owner_gid_id', sa.Integer(), nullable=True),
    sa.Column('tour_name', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('region', sa.String(), nullable=False),
    sa.Column('photos', sa.JSON(), nullable=True),
    sa.Column('map_points', sa.JSON(), nullable=False),
    sa.Column('tour_description', sa.String(), nullable=False),
    sa.Column('complexity', sa.String(), nullable=False),
    sa.Column('free_services', sa.JSON(), nullable=True),
    sa.Column('additional_services', sa.JSON(), nullable=True),
    sa.Column('recommended_min_age', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['owner_gid_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tour_plan',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('schema_id', sa.UUID(), nullable=True),
    sa.Column('date_from', sa.TIMESTAMP(), nullable=False),
    sa.Column('date_to', sa.TIMESTAMP(), nullable=False),
    sa.Column('meeting_point', sa.String(), nullable=False),
    sa.Column('meeting_datetime', sa.TIMESTAMP(), nullable=False),
    sa.Column('max_person', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['schema_id'], ['tour_schema.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tour_offer',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('tour_plan_id', sa.UUID(), nullable=True),
    sa.Column('tourist_id', sa.Integer(), nullable=True),
    sa.Column('booking_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('tourists_amount', sa.Integer(), nullable=False),
    sa.Column('payment_state', sa.Boolean(), nullable=False),
    sa.Column('cancellation', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['tour_plan_id'], ['tour_plan.id'], ),
    sa.ForeignKeyConstraint(['tourist_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tour_offer')
    op.drop_table('tour_plan')
    op.drop_table('tour_schema')
    # ### end Alembic commands ###
