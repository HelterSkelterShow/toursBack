from typing import Optional, List
import json
from fastapi import UploadFile
from fastapi import Form
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

   # @staticmethod
   # def list_of_lists_converter(mapPoints):
   #     cleaned_s = mapPoints.replace('"', '')
   #     list_of_lists = [[float(num) for num in sublist.split(',')] for sublist in cleaned_s.strip('[]').split('],[')]
   #     return list_of_lists
   #
   # @staticmethod
   # def list_converter(s):
   #     cleaned_s = s.replace('"', '')
   #     list_of_elems = [str(service) for service in cleaned_s.strip('[]').split('],[')]
   #     return list_of_elems
   #
   # @classmethod
   # def as_form(
   #         cls,
   #         tourName: str = Form(),
   #         category: str = Form(),
   #         region: str = Form(),
   #         mapPoints: str = Form(),
   #         tourDescription: str = Form(),
   #         complexity: str = Form(),
   #         recommendedAgeFrom: int = Form(),
   #         recommendedAgeTo: int = Form(),
   #         freeServices: Optional[str] = Form(default=None),
   #         additionalServices: Optional[str] = Form(default=None),
   #    ):
   #     return cls(tourName=tourName,
   #                category=category,
   #                region = region,
   #                mapPoints = TourTempl.list_of_lists_converter(mapPoints),
   #                tourDescription = tourDescription,
   #                complexity = complexity,
   #                recommendedAgeFrom = recommendedAgeFrom,
   #                recommendedAgeTo = recommendedAgeTo,
   #                freeServices = TourTempl.list_converter(freeServices) if freeServices is not None else None,
   #                additionalServices = TourTempl.list_converter(additionalServices) if additionalServices is not None else None
   #                )

# class TourTemplUpdate(BaseModel):
#    tourName: str
#    category: str
#    region: str
#    mapPoints: List[List[float]]
#    tourDescription: str
#    complexity: str
#    recommendedAgeFrom: int
#    recommendedAgeTo: int
#    freeServices: Optional[List[str]]
#    additionalServices: Optional[List[str]]
#    tourPhotos: Optional[List[str]]
   #
   # @staticmethod
   # def list_of_lists_converter(mapPoints):
   #     cleaned_s = mapPoints.replace('"', '')
   #     list_of_lists = [[float(num) for num in sublist.split(',')] for sublist in cleaned_s.strip('[]').split('],[')]
   #     return list_of_lists
   #
   # @staticmethod
   # def list_converter(s):
   #     cleaned_s = s.replace('"', '')
   #     list_of_elems = [str(service) for service in cleaned_s.strip('[]').split('],[')]
   #     return list_of_elems
   #
   # @classmethod
   # def as_form(
   #         cls,
   #         tourName: str = Form(),
   #         category: str = Form(),
   #         region: str = Form(),
   #         mapPoints: str = Form(),
   #         tourDescription: str = Form(),
   #         complexity: str = Form(),
   #         recommendedAgeFrom: int = Form(),
   #         recommendedAgeTo: int = Form(),
   #         freeServices: Optional[str] = Form(default=None),
   #         additionalServices: Optional[str] = Form(default=None),
   #         tourPhotos: Optional[str] = Form(default=None)
   #    ):
   #     return cls(tourName=tourName,
   #                category=category,
   #                region = region,
   #                mapPoints = TourTempl.list_of_lists_converter(mapPoints),
   #                tourDescription = tourDescription,
   #                complexity = complexity,
   #                recommendedAgeFrom = recommendedAgeFrom,
   #                recommendedAgeTo = recommendedAgeTo,
   #                freeServices = TourTempl.list_converter(freeServices) if freeServices is not None else None,
   #                additionalServices = TourTempl.list_converter(additionalServices) if additionalServices is not None else None,
   #                tourPhotos = TourTempl.list_converter(tourPhotos) if tourPhotos is not None else None
   #                )

