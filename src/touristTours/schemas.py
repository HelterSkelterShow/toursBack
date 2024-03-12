import datetime
import uuid
from typing import List
from pydantic import BaseModel

class Price(BaseModel):
    min: int|None = None
    max: int|None = None

class recommendedAge(BaseModel):
    ageFrom: int|None = None
    ageTo: int|None = None

class Dates(BaseModel):
    dateFrom: datetime.datetime|None = None
    dateTo: datetime.datetime|None = None

class TourSearchRq(BaseModel):
    region: str|None = None
    tourdate: Dates|None = None
    complexity: List[str]|None = None
    category: List[str]|None = None
    prices: Price|None = None
    maxPerson: int|None = None
    toursDuration: int|None = None
    searchParam: str|None = None

class TourSearchRs(BaseModel):
    id: str
    tourName: str
    photos: str
    category: str
    price: int
    region: str
    dateFrom: datetime.datetime
    dateTo: datetime.datetime

class pagination(BaseModel):
    page: int
    perPage: int
    hasMore: bool


class RsList(BaseModel):
    status: str
    data: List[TourSearchRs]
    details: pagination

class TourData(BaseModel):
    id: str
    creatorName: str
    tourName: str
    price: int
    region: str
    category: str
    photos: List[str]
    dateFrom: datetime.datetime
    dateTo: datetime.datetime
    meetingPoint: str
    meetingDatetime: datetime.datetime
    maxPersonNumber: int
    complexity: str
    mapPoints: List[List[int]]
    tourDescription: str
    freeServices: List[str]
    additionalServices: List[str]
    recommendedAgeFrom: int
    recommendedAgeTo: int

class TourResponse(BaseModel):
    status: str
    data: TourData
    details: str|None = None