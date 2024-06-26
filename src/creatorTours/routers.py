import json
import math
import uuid
import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, delete, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
import boto3
from src.config import AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, TIME_TO_UPDATE, TIME_TO_CANCEL, COMMISSION

from src.creatorTours.models import tour_schema, tours_plan, offers
from src.creatorTours.utils import photosOptimization
from src.auth.models import User
from src.database import get_async_session
from src.creatorTours.schemas import TourTempl, publicTour, publicTourUpdate, TourListResponse, \
    TemplateSearchRs
from src.touristTours.schemas import Dates

router = APIRouter(
    prefix="/creator/tours",
    tags=["creatorTours"]
)

@router.post("/templates/create")
async def createTourTemplate(templ: TourTempl,
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)) -> dict:
    try:
        query = insert(tour_schema).values(
            tourId = uuid.uuid4(),
            ownerGidId = user.id,
            tourName = templ.tourName,
            category = templ.category,
            region = templ.region,
            mapPoints = templ.mapPoints,
            photos = templ.tourPhotos,
            tourDescription = templ.tourDescription,
            complexity = templ.complexity,
            freeServices = templ.freeServices,
            additionalServices = templ.additionalServices,
            recommendedAgeFrom = templ.recommendedAgeFrom,
            recommendedAgeTo = templ.recommendedAgeTo,
            isArchived = False
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
                             templ: TourTempl,
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)) -> dict:
    try:
        query = select(tour_schema.c.photos).where(tour_schema.c.tourId == id)
        result = await session.execute(query)
        client = boto3.client(service_name="s3",
                              endpoint_url='https://storage.yandexcloud.net',
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        tourPhotos = templ.tourPhotos if templ.tourPhotos != None else []
        for image in result.all()[0][0]:
            if image not in tourPhotos:
                client.delete_object(Bucket='mywaytours',
                                     Key=image.removeprefix('https://storage.yandexcloud.net/mywaytours/'))
    except:
        raise HTTPException(500, detail={
            "status": "S3_ERROR",
            "data": None,
            "details": None
        })
    try:
        query = update(tour_schema).where(tour_schema.c.tourId == id).values(
            ownerGidId=user.id,
            tourName=templ.tourName,
            category=templ.category,
            region=templ.region,
            mapPoints=templ.mapPoints,
            photos=templ.tourPhotos,
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
    # try:
        stmt = tour_schema.join(tours_plan, tour_schema.c.tourId == tours_plan.c.schemaId)
        stmt_query = stmt.select().with_only_columns(tours_plan.c.id.label('publicTourId'), tours_plan.c.dateFrom, tours_plan.c.dateTo)
        total_count = await session.execute(stmt_query.with_only_columns(func.count().label('total')))
        total = total_count.scalar()
        # if total > 0:
        #     result = await session.execute(stmt_query)
        #     res_list = result.mappings().all()
        #     list_of_dicts = [dict(row) for row in res_list]
        #     for public in list_of_dicts:
        #         public["publicTourId"] = str(public["publicTourId"])
        #         public["cancelDeadline"] = (public["dateFrom"] - datetime.timedelta(days=TIME_TO_CANCEL)).strftime('%Y-%m-%d')
        #         public["dateFrom"] = (public["dateFrom"]).strftime('%Y-%m-%d')
        #         public["dateTo"] = (public["dateTo"]).strftime('%Y-%m-%d')
        #     raise HTTPException(status_code=300, detail={
        #         "status": "redirect",
        #         "data": list_of_dicts,
        #         "details": "There are several publications, connected with the template"
        #     })
        # query = select(tour_schema.c.photos).where(tour_schema.c.tourId == id)
        # result = await session.execute(query)
        # client = boto3.client(service_name="s3",
        #                       endpoint_url='https://storage.yandexcloud.net',
        #                       aws_access_key_id=AWS_ACCESS_KEY_ID,
        #                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        # for image in result.all()[0][0]:
        #     client.delete_object(Bucket='mywaytours', Key=image.removeprefix('https://storage.yandexcloud.net/mywaytours/'))
        # stmt = delete(tour_schema).where(tour_schema.c.tourId == id)
        stmt = update(tour_schema)\
            .where(tour_schema.c.tourId == id)\
            .values(isArchived = True)
        await session.execute(stmt)
        await session.commit()
        return {"status":"success",
                "data":None,
                "details":None
                }
    # except:
    #     raise HTTPException(status_code=500, detail={
    #          "status": "error",
    #          "data": None,
    #          "details": None
    #      })

@router.get("/templates/{id}")
async def getTourTemplate(id: str,
                          user: User = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = select(tour_schema).where(tour_schema.c.tourId == id)
        result = await session.execute(query)
        res_dict = dict(result.mappings().first())

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

@router.get("/templates", response_model=TemplateSearchRs)
async def getTourTemplateList(isArchived: bool, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(tour_schema.c.tourId, tour_schema.c.tourName, tour_schema.c.category,
                       tour_schema.c.photos, tour_schema.c.region, tour_schema.c.complexity)\
            .where((tour_schema.c.ownerGidId == user.id) & (tour_schema.c.isArchived == isArchived))
        result = await session.execute(query)
        res_list = result.mappings().all()
        list_of_tours = photosOptimization(res_list)

        for templates in list_of_tours:
            stmt = tour_schema.join(tours_plan, tours_plan.c.schemaId == tour_schema.c.tourId)
            stmt_query = stmt.select()\
                .where((tour_schema.c.tourId == templates["tourId"]) & (tours_plan.c.state == "isActive") & (tours_plan.c.dateFrom > datetime.datetime.utcnow()))
            total_count = await session.execute(stmt_query.with_only_columns(func.count().label('total')))
            total = total_count.scalar()
            templates["publicCount"] = total
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

@router.post("/templates/activate")
async def activateTemplate(id: uuid.UUID, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    stmt = update(tour_schema) \
        .where(tour_schema.c.tourId == id) \
        .values(isArchived=False)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success",
            "data": None,
            "details": None
            }

@router.post("/public/create")
async def publicTourCreate(public: publicTour, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = insert(tours_plan).values(
            id = uuid.uuid4(),
            schemaId = public.tourId,
            price = public.tourAmount,
            dateFrom = public.dateFrom,
            dateTo = public.dateTo,
            meetingPoint = public.meetingPoint,
            meetingDatetime = public.meetingTime,
            maxPersonNumber = public.maxPersonNumber,
        )
        await session.execute(query)
        await session.commit()

        stmt = tour_schema.join(tours_plan, tour_schema.c.tourId == tours_plan.c.schemaId)
        query = stmt.select().with_only_columns(tour_schema.c.tourName, tours_plan.c.id).where(tour_schema.c.tourId == public.tourId)
        result = await session.execute(query)
        res_dict = dict(result.mappings().first())
    except:
        raise HTTPException(500, detail={
            "status":"DB_ERROR",
            "data":None,
            "details":"Error while inserting tour template into database"
        })
    return {
        "status": "success",
        "data": {"publicTourId": res_dict["id"],
                 "tourName": res_dict["tourName"],
                 "cancelDeadline": public.dateFrom - datetime.timedelta(days=TIME_TO_CANCEL),
                 },
        "details": None
    }

@router.delete("/public/{id}")
async def publicDelete(id: str, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = update(tours_plan).where(tours_plan.c.id == id).values(
            state="cancelled"
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
        "data": None,
        "details": None
    }

@router.get("/public", response_model=TourListResponse)
async def publicGetList(year: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        stmt = tour_schema.join(tours_plan, tour_schema.c.tourId == tours_plan.c.schemaId).join(User, tour_schema.c.ownerGidId == User.id)

        query = stmt.select().with_only_columns(tour_schema.c.tourId, tours_plan.c.id.label('publicTourId'), tour_schema.c.tourName, tours_plan.c.price.label('tourAmount'),
                                                tours_plan.c.meetingPoint, tours_plan.c.meetingDatetime.label('meetingTime'),
                                                tours_plan.c.maxPersonNumber, tours_plan.c.dateFrom, tours_plan.c.dateTo,
                                                tours_plan.c.state.label('state'))\
            .filter((tours_plan.c.dateTo > datetime.datetime(year - 1, 1, 1)) & (tours_plan.c.dateFrom < datetime.datetime(year + 2, 1, 1))
                    & ((tours_plan.c.state == "isActive") | (tours_plan.c.state == "finished")) & (tour_schema.c.ownerGidId == user.id))
        result = await session.execute(query)
        res_dict = result.mappings().all()
        list_of_dicts = [dict(row) for row in res_dict]



        for tour in list_of_dicts:
            query_profit = offers.select().with_only_columns(func.sum(offers.c.tourAmount)).filter(
                offers.c.tourPlanId == tour["publicTourId"])
            amount_res = await session.execute(query_profit)
            amount_res = amount_res.scalar()

            tour["cancelDeadline"] = tour["dateFrom"] - datetime.timedelta(days=TIME_TO_CANCEL)

            if amount_res != None:
                tour["profit"] = int(math.ceil(amount_res/COMMISSION))
            else:
                tour["profit"] = 0

            stmt = offers.join(User, User.id == offers.c.touristId)
            query = stmt.select().with_only_columns(User.name, User.email, User.phone ,offers.c.id.label('bookingId'), offers.c.cancellation,
                                                      offers.c.bookingTime, offers.c.tourAmount,
                                                      offers.c.tourists, offers.c.comment) \
                .filter((offers.c.tourPlanId == tour["publicTourId"]) & (offers.c.cancellation == False))
            bookings_res = await session.execute(query)
            bookings_res = bookings_res.mappings().all()
            list_of_bookings = [dict(row) for row in bookings_res]
            for booking in list_of_bookings:
                booking["tourists"] = json.loads(booking["tourists"])
            tour["bookingInfo"] = list_of_bookings

        return {"status": "success",
                "data": list_of_dicts,
                "details": None
                }
    except:
        raise HTTPException(500, detail={
            "status": "ERROR",
            "data": None,
            "details": "NOT FOUND"
        })

@router.post("/statistics")
async def getStatistics(date: Dates, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    stmt = tour_schema.join(tours_plan, tour_schema.c.tourId == tours_plan.c.schemaId).join(offers, tours_plan.c.id == offers.c.tourPlanId)
    query = stmt.select().with_only_columns(tour_schema.c.tourName,
                                            func.sum(offers.c.touristsAmount).label('touristsAmount'),
                                            func.sum(offers.c.tourAmount).label('tourAmount')) \
        .filter((tour_schema.c.ownerGidId == user.id) & (tours_plan.c.dateFrom >= date.dateFrom) & (tours_plan.c.dateFrom <= date.dateTo) & \
                ((tours_plan.c.state == "isActive") | (tours_plan.c.state == "finished")) & (offers.c.cancellation == False))\
        .group_by(tour_schema.c.tourName)
    result = await session.execute(query)
    result = result.mappings().all()
    list_of_dicts = [dict(row) for row in result]
    for tour in list_of_dicts:
        tour["tourAmount"] = math.ceil(tour["tourAmount"]/COMMISSION)
    return {
        "status":"success",
        "data":list_of_dicts,
        "details":None
    }




