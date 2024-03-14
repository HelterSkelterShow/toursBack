import datetime
import uuid
from typing import Optional, List
from pydantic import BaseModel

class Tourist(BaseModel):
    name: str
    birthDate: datetime.datetime

class BookingRq(BaseModel):
    publicTourId: uuid.UUID
    tourAmount: int
    tourists: List[Tourist]
    comment: str | None = None