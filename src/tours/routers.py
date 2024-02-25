import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.base_config import current_user
import boto3
from src.config import AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_DEFAULT_REGION

from src.tours.models import tour_schema, tours_plan, offers
from src.auth.models import User
from src.database import get_async_session
from src.tours.schemas import TourSearchRq, RsList, TourTemplCreateRq

router = APIRouter(
    prefix="/tours",
    tags=["tours"]
)

@router.post("/template/create")
async def createTourTemplate(tourPhotos: List[UploadFile],
                             templ: TourTemplCreateRq = Depends(TourTemplCreateRq.as_form),
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)) -> dict:
    for tempFile in tourPhotos:
        if tempFile.content_type not in ("image/jpeg", "image/png"):
            raise HTTPException(400, detail={
                "status":"ERROR",
                "data":None,
                "details":"Invalid document type"
            })
    try:
        photosPath = []
        for tempFile in tourPhotos:
            id = uuid.uuid4()
            url = f"https://storage.yandexcloud.net/mywaytours/{id}"
            photosPath.append(url)
            client = boto3.client(service_name = "s3",
                                  endpoint_url='https://storage.yandexcloud.net',
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

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
            "details":"Error while insrting tour template into database"
        })
    return {
        "status": "success",
        "data": templ,
        "details": None
    }