import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.base_config import current_user
import boto3
from src.config import AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, MAX_FILE_SIZE, MAX_FILE_SUM_SIZE

from src.tours.models import tour_schema, tours_plan, offers
from src.tours.utils import fileValidation
from src.auth.models import User
from src.database import get_async_session
from src.tours.schemas import TourSearchRq, RsList, TourTemplCreateRq

router = APIRouter(
    prefix="/tours",
    tags=["tours"]
)

@router.post("/templates/create")
async def createTourTemplate(tourPhotos: List[UploadFile],
                             templ: TourTemplCreateRq = Depends(TourTemplCreateRq.as_form),
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
            id = uuid.uuid4(),
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
                             tourPhotos: List[UploadFile],
                             templ: TourTemplCreateRq = Depends(TourTemplCreateRq.as_form),
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)) -> dict:
    fileValidation(tourPhotos)
    try:
        query = select(tour_schema.c.photos).where(tour_schema.c.id == id)
        result = await session.execute(query)
        client = boto3.client(service_name="s3",
                              endpoint_url='https://storage.yandexcloud.net',
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        for image in result.all()[0][0]:
            client.delete_object(Bucket='mywaytours',
                                 Key=image.removeprefix('https://storage.yandexcloud.net/mywaytours/'))
        photosPath = []
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
        query = update(tour_schema).where(tour_schema.c.id == id).values(
            id=id,
            ownerGidId=user.id,
            tourName=templ.tourName,
            category=templ.category,
            region=templ.region,
            mapPoints=templ.mapPoints,
            photos=photosPath,
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
        query = select(tour_schema.c.photos).where(tour_schema.c.id == id)
        result = await session.execute(query)
        client = boto3.client(service_name="s3",
                              endpoint_url='https://storage.yandexcloud.net',
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        for image in result.all()[0][0]:
            client.delete_object(Bucket='mywaytours', Key=image.removeprefix('https://storage.yandexcloud.net/mywaytours/'))
        stmt = delete(tour_schema).where(tour_schema.c.id == id)
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

