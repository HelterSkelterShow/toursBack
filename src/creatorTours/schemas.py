import datetime
import uuid
from typing import Optional, List
from pydantic import BaseModel

from src.bookings.schemas import Tourist


class publicTour(BaseModel):
    tourId: str
    tourAmount: int
    dateFrom: datetime.datetime
    dateTo: datetime.datetime
    meetingPoint: str
    meetingTime: datetime.datetime
    maxPersonNumber:int

class publicTourUpdate(BaseModel):
    tourAmount: int
    dateFrom: datetime.datetime
    dateTo: datetime.datetime
    meetingPoint: str
    meetingTime: datetime.datetime
    maxPersonNumber:int

class RecomendedAge(BaseModel):
    recommendedAgeFrom:int
    recommendedAgeTo:int

class TourTempl(BaseModel):
   tourName: str
   category: str
   region: str
   mapPoints: List[List[float]]
   tourDescription: str
   complexity: str
   recommendedAgeFrom: int
   recommendedAgeTo: int
   freeServices: List[str]|None = None
   additionalServices: List[str]|None = None
   tourPhotos: List[str]|None = None

class TourResponseData(BaseModel):
    schemaId: str
    price: int
    dateFrom: datetime.datetime
    dateTo: datetime.datetime
    meetingPoint: str
    meetingDateTime: datetime.datetime
    maxPersonNumber: int

class TourResponse(BaseModel):
    status: str
    data: TourResponseData
    details: str|None = None

class BookingInfo(BaseModel):
    bookingId: uuid.UUID
    cancellation: bool
    bookingTime: datetime.datetime
    tourAmount: int
    tourists: List[Tourist]
    comment: str
    name: str
    email: str
    phone: str

class TourListData(BaseModel):
    tourId: uuid.UUID
    publicTourId: uuid.UUID
    tourName: str
    tourAmount: int
    meetingPoint: str
    meetingTime: datetime.datetime
    maxPersonNumber: int
    dateFrom: datetime.datetime
    dateTo: datetime.datetime
    cancelDeadline: datetime.datetime
    bookingInfo: List[BookingInfo]
    state: str
    profit: int

class TourListResponse(BaseModel):
    status: str
    data: List[TourListData]
    details: str|None = None

class TemplateListRs(BaseModel):
    tourId: uuid.UUID
    tourName: str
    photos: str
    publicCount: int
    category: str
    region: str
    complexity: str

class TemplateSearchRs(BaseModel):
    status: str
    data: List[TemplateListRs]
    details: str|None = None

class Dates:
    dateFrom: datetime.datetime
    dateTo: datetime.datetime

