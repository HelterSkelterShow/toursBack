import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
import boto3
from src.config import AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID

from src.tours.models import tour_schema
from src.tours.utils import fileValidation, photosOptimization, updatePhotos
from src.auth.models import User
from src.database import get_async_session
from src.tours.schemas import TourTempl

router = APIRouter(
    prefix="/tours",
    tags=["tours"]
)

@router.post("/templates/create")
async def createTourTemplate(tourPhotos: List[UploadFile],
                             templ: TourTempl = Depends(TourTempl.as_form_create),
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)) -> dict:
    fileValidation(tourPhotos)
    try:
        photosPath = []
        client = boto3.client(service_name="s3",
                              endpoint_url='https://storage.yandexcloud.net',
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

        for tempFile in tourPhotos:
            id = uuid.uuid4()
            url = f"https://storage.yandexcloud.net/mywaytours/{id}"
            photosPath.append(url)
            client.upload_fileobj(tempFile.file, 'mywaytours', str(id))
    except:
        raise HTTPException(500, detail={
            "status": "S3_ERROR",
            "data": None,
            "details": None
        })

    try:
        query = insert(tour_schema).values(
            tourId = uuid.uuid4(),
            ownerGidId = user.id,
            tourName = templ.tourName,
            category = templ.category,
            region = templ.region,
            mapPoints = templ.mapPoints,
            photos = photosPath,
            tourDescription = templ.tourDescription,
            complexity = templ.complexity,
            freeServices = templ.freeServices,
            additionalServices = templ.additionalServices,
            recommendedAgeFrom = templ.recommendedAgeFrom,
            recommendedAgeTo = templ.recommendedAgeTo
        )
        await session.execute(query)
        await session.commit()
    except:
        raise HTTPException(500, detail={
            "status":"DB_ERROR",
            "data":None,
            "details":"Error while inserting tour template into database"
        })
    return {
        "status": "success",
        "data": templ,
        "details": None
    }

@router.put("/templates/{id}")
async def updateTourTemplate(id: str,
                             newPhotos: List[UploadFile],
                             templ: TourTempl = Depends(TourTempl.as_form_update),
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)) -> dict:
    fileValidation(newPhotos)

    try:
        query = select(tour_schema.c.photos).where(tour_schema.c.tourId == id)
        result = await session.execute(query)
        client = boto3.client(service_name="s3",
                              endpoint_url='https://storage.yandexcloud.net',
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        tourPhotos = templ.oldPhotos if templ.oldPhotos != None else []
        for image in result.all()[0][0]:
            if image not in tourPhotos:
                client.delete_object(Bucket='mywaytours',
                                     Key=image.removeprefix('https://storage.yandexcloud.net/mywaytours/'))

        tourPhotos = updatePhotos(tourPhotos, newPhotos, client)
    except:
        raise HTTPException(500, detail={
            "status": "S3_ERROR",
            "data": None,
            "details": None
        })
    try:
        print(templ.oldPhotos)
        query = update(tour_schema).where(tour_schema.c.tourId == id).values(
            ownerGidId=user.id,
            tourName=templ.tourName,
            category=templ.category,
            region=templ.region,
            mapPoints=templ.mapPoints,
            photos=tourPhotos,
            tourDescription=templ.tourDescription,
            complexity=templ.complexity,
            freeServices=templ.freeServices,
            additionalServices=templ.additionalServices,
            recommendedAgeFrom=templ.recommendedAgeFrom,
            recommendedAgeTo=templ.recommendedAgeTo
        )
        await session.execute(query)
        await session.commit()
    except:
        raise HTTPException(500, detail={
            "status": "DB_ERROR",
            "data": None,
            "details": "Error while inserting tour template into database"
        })
    return {
        "status": "success",
        "data": templ,
        "details": f"Tour template {id} successfully updated!"
    }

@router.delete("/templates/{id}")
async def deleteTourTemplate(id: str,
                                 user: User = Depends(current_user),
                                 session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = select(tour_schema.c.photos).where(tour_schema.c.tourId == id)
        result = await session.execute(query)
        client = boto3.client(service_name="s3",
                              endpoint_url='https://storage.yandexcloud.net',
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        for image in result.all()[0][0]:
            client.delete_object(Bucket='mywaytours', Key=image.removeprefix('https://storage.yandexcloud.net/mywaytours/'))
        stmt = delete(tour_schema).where(tour_schema.c.tourId == id)
        await session.execute(stmt)
        await session.commit()
        return {"status":"success",
                "data":None,
                "details":None
                }
    except:
        raise HTTPException(status_code=500, detail={
             "status": "error",
             "data": None,
             "details": None
         })

@router.get("/templates/{id}")
async def getTourTemplate(id: str,
                          user: User = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = select(tour_schema).where(tour_schema.c.tourId == id)
        result = await session.execute(query)
        res_dict = dict(result.mappings().first())

        if res_dict["freeServices"] != None:
            res_dict["freeServices"] = res_dict["freeServices"][0].split(",")
            res_dict["freeServices"] = [item.encode('utf-8') for item in res_dict["freeServices"]]
        if res_dict["additionalServices"] != None:
            res_dict["additionalServices"] = res_dict["additionalServices"][0].split(",")
            res_dict["additionalServices"] = [item.encode('utf-8') for item in res_dict["additionalServices"]]

        return {"status": "success",
                "data": res_dict,
                "details": None
                }
    except:
        raise HTTPException(500, detail={
            "status":"ERROR",
            "data":None,
            "details":"NOT FOUND"
        })

@router.get("/templates")
async def getTourTemplateList(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(tour_schema.c.tourId, tour_schema.c.tourName, tour_schema.c.photos)
        result = await session.execute(query)
        res_list = result.mappings().all()
        list_of_tours = photosOptimization(res_list)
        return {"status": "success",
                "data": list_of_tours,
                "details": None
                }
    except:
        raise HTTPException(500, detail={
            "status":"ERROR",
            "data":None,
            "details":"NOT FOUND"
        })





