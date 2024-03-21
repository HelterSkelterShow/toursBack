from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData, UUID, DateTime
from sqlalchemy.orm import relationship

from src.auth.models import User
from src.database import Base, metadata

tour_schema = Table(
    "tour_schema",
    metadata,
    Column("tourId", UUID, primary_key=True),
    Column("ownerGidId", Integer, ForeignKey(User.id)),
    Column("tourName", String, nullable=False),
    Column("category", String, nullable=False),
    Column("region", String, nullable=False),
    Column("photos", JSON, nullable=True),
    Column("mapPoints", JSON, nullable=False),
    Column("tourDescription", String, nullable=False),
    Column("complexity", String, nullable=False),
    Column("freeServices", JSON, nullable=True),
    Column("additionalServices", JSON, nullable=True),
    Column("recommendedAgeFrom", Integer, nullable=False),
    Column("recommendedAgeTo", Integer, nullable=False)
)

tours_plan = Table(
    "tour_plan",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("schemaId", UUID, ForeignKey(tour_schema.c.tourId)),
    Column("price", Integer, nullable=False),
    Column("dateFrom", TIMESTAMP(timezone=True), nullable=False),
    Column("dateTo", TIMESTAMP(timezone=True) , nullable=False),
    Column("meetingPoint", String, nullable=False),
    Column("meetingDatetime", TIMESTAMP(timezone=True) , nullable=False),
    Column("maxPersonNumber", Integer, nullable=False),
    Column("state", String, default="isActive"),
    Column("isFull", Boolean, default=False)
)

offers = Table(
    "tour_offer",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("tourPlanId", UUID, ForeignKey(tours_plan.c.id)),
    Column("touristId", Integer, ForeignKey(User.id)),
    Column("bookingTime", TIMESTAMP(timezone=True), default=datetime.utcnow),
    Column("tourAmount", Integer, nullable=False),
    Column("tourists", JSON, nullable=False),
    Column("cancellation", Boolean, default=False),
    Column("comment", String, nullable=True),
    Column("touristsAmount", Integer, nullable=False)
)