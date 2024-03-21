from datetime import datetime
import enum

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData, UUID, DateTime

from src.auth.models import User
from src.creatorTours.models import tours_plan
from src.database import Base, metadata

claims = Table(
    "claim",
    metadata,
    Column("claimId", Integer, primary_key=True, autoincrement=True),
    Column("touristId", Integer, ForeignKey(User.id)),
    Column("gidEmail", String, nullable=True),
    Column("description", String, nullable=False),
    Column("publicTourId", UUID, ForeignKey(tours_plan.c.id), nullable=True),
    Column("state", String, default="consideration"),
    Column("creationDateTime", TIMESTAMP(timezone=True), default=datetime.utcnow),
    Column("type", String, nullable=True)
)
