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

class Tour(BaseModel):
    tourId: uuid.UUID
    tourName: str
    additionalServices: List[str]|None = None
    freeServices: List[str]|None = None
    mapPoints: List[List[float]]

class Contact(BaseModel):
    name: str
    email: str
    phone: str

class bookedTour(BaseModel):
    statusBooking: str
    dateFrom: datetime.datetime
    dateTo: datetime.datetime
    publicTourId: uuid.UUID
    bookingId: uuid.UUID
    tourAmount: int
    contactInformation: Contact
    meetingPoint: str
    meetingTime: datetime.datetime
    cancelDeadline: datetime.datetime
    tour: Tour

class bookings(BaseModel):
    data: List[bookedTour]