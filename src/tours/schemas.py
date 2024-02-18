from typing import Optional, List
from pydantic import BaseModel

class Price(BaseModel):
    min: Optional[int]
    max: Optional[int]

class Dates(BaseModel):
    dateFrom: str
    dateTo: str

class TourSearchRq(BaseModel):
    region: Optional[str]
    dateFrom: Optional[str]
    dateTo: Optional[str]
    complexity: Optional[List[str]]
    category: Optional[List[str]]
    prices: Optional[Price]
    maxPerson: Optional[int]

class TourSearchRs(BaseModel):
    id: str
    tourName: str
    photos: List[str]
    category: str
    complexity: str
    price: int
    region: str
    tourDate: Dates
    maxPersonNumber: int

class RsList(BaseModel):
    hasNew: bool
    tours: List[TourSearchRs]




