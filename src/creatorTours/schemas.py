import datetime
import uuid
from typing import Optional, List
from pydantic import BaseModel



class Dates(BaseModel):
    dateFrom: datetime.datetime
    dateTo: datetime.datetime

class publicTour(BaseModel):
    tourId: str
    tourAmount: int
    date: Dates
    meetingPoint: str
    meetingTime: datetime.datetime
    maxPersonNumber:int

class publicTourUpdate(BaseModel):
    price: int
    date: Dates
    meetingPoint: str
    meetingDateTime: datetime.date
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
    date: Dates
    meetingPoint: str
    meetingDateTime: datetime.datetime
    maxPersonNumber: int

class TourResponse(BaseModel):
    status: str
    data: TourResponseData
    details: str|None = None


class TourListData(BaseModel):
    tourId: str
    tourName: str
    price: int
    meetingPoint: str
    meetingDatetime: datetime.datetime
    maxPersonNumber: int
    dateFrom: datetime.datetime
    dateTo: datetime.datetime
    cancelDeadline: datetime.datetime
    updateDeadline: datetime.datetime

class TourListResponse(BaseModel):
    status: str
    data: List[TourListData]
    details: str|None = None

class TemplateListRs(BaseModel):
    tourId: uuid.UUID
    tourName: str
    photos: str
    publicCount: int

class TemplateSearchRs(BaseModel):
    status: str
    data: List[TemplateListRs]
    details: Optional[str]
