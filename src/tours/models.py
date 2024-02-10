from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData, UUID

from src.database import Base, metadata
from src.auth.models import user

tour_schema = Table(
    "tour_schema",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("owner_gid_id", Integer, ForeignKey(user.c.id)),
    Column("tour_name", String, nullable=False),
    Column("category", String, nullable=False),
    Column("region", String, nullable=False),
    Column("photos", JSON, nullable=True),
    Column("map_points", JSON, nullable=False),
    Column("tour_description", String, nullable=False),
    Column("complexity", String, nullable=False),
    Column("free_services", JSON, nullable=True),
    Column("additional_services", JSON, nullable=True),
    Column("recommended_min_age", String, nullable=False)
)

tours_plan = Table(
    "tour_plan",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("schema_id", UUID, ForeignKey(tour_schema.c.id)),
    Column("date_from", TIMESTAMP, nullable=False),
    Column("date_to", TIMESTAMP, nullable=False),
    Column("meeting_point", String, nullable=False),
    Column("meeting_datetime", TIMESTAMP, nullable=False),
    Column("max_person", Integer, nullable=False)
)

offers = Table(
    "tour_offer",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("tour_plan_id", UUID, ForeignKey(tours_plan.c.id)),
    Column("tourist_id", Integer, ForeignKey(user.c.id)),
    Column("booking_time", TIMESTAMP, default=datetime.utcnow),
    Column("tourists_amount", Integer, nullable=False),
    Column("payment_state", Boolean, nullable=False),
    Column("cancellation", Boolean, default=False)
)