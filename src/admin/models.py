from datetime import datetime
import enum

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData, UUID, DateTime

from src.auth.models import User
from src.creatorTours.models import tours_plan
from src.database import Base, metadata

claims = Table(
    "claims",
    metadata,
    Column("claimId", UUID, primary_key=True),
    Column("touristId", Integer, ForeignKey(User.id)),
    Column("gidEmail", String, nullable=False),
    Column("description", String, nullable=False),
    Column("publicTourId", UUID, ForeignKey(tours_plan.c.id)),
    Column("state", String, default="consideration"),
    Column("creationDateTime", TIMESTAMP, default=datetime.utcnow),
)
