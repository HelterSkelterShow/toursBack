import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, insert, update

from src.admin.models import claims
from src.auth.base_config import current_user
from src.auth.models import User
from src.config import TOURS_PER_PAGE
from src.creatorTours.models import tour_schema, tours_plan, offers
from src.creatorTours.utils import photosOptimization
from src.database import get_async_session
from src.touristTours.schemas import TourSearchRq, RsList, TourResponse, claimRq, questRq

router = APIRouter(
    prefix="/tours",
    tags=["user"]
)

@router.post("/search", response_model=RsList)
async def toursSearch(searchRq: TourSearchRq, page: int = Query(gt=0), perPage: int = TOURS_PER_PAGE,  session: AsyncSession = Depends(get_async_session)) -> dict:
    # try:
        stmt = tour_schema.join(tours_plan, tour_schema.c.tourId == tours_plan.c.schemaId)
        query = stmt.select().with_only_columns(tours_plan.c.id.label('tourId'), tour_schema.c.tourName, tours_plan.c.price,
                                                tour_schema.c.region, tour_schema.c.category,
                                                tour_schema.c.photos, tours_plan.c.dateFrom,
                                                tours_plan.c.dateTo, tours_plan.c.state)
        query = query.filter(tours_plan.c.dateFrom >= datetime.now())
        query = query.filter(tours_plan.c.state == "isActive")
  #      query = query.filter(tour_schema.c.isFull == False)

        if searchRq.tourdate:
            if searchRq.tourdate.dateFrom:
                query = query.filter(tours_plan.c.dateFrom >= searchRq.tourdate.dateFrom)
            if searchRq.tourdate.dateTo:
                query = query.filter(tours_plan.c.dateTo <= searchRq.tourdate.dateTo)
        if searchRq.region:
            query = query.filter(tour_schema.c.region == searchRq.region)

        if searchRq.complexity:
            query = query.filter(tour_schema.c.complexity.in_(searchRq.complexity))

        if searchRq.category:
            query = query.filter(tour_schema.c.category.in_(searchRq.category))

        if searchRq.prices:
            if searchRq.prices.min:
                query = query.filter(tours_plan.c.price > searchRq.prices.min)
            if searchRq.prices.max:
                query = query.filter(tours_plan.c.price < searchRq.prices.max)

        if searchRq.recommendedAge:
            if searchRq.recommendedAge.min:
                query = query.filter(tour_schema.c.recommendedAgeFrom >= searchRq.recommendedAge.min)
            if searchRq.recommendedAge.max:
                query = query.filter(tour_schema.c.recommendedAgeTo <= searchRq.recommendedAge.max)

        if searchRq.maxPerson:
            query = query.filter(tours_plan.maxPerson >= searchRq.maxPerson)
        if searchRq.searchParam:
            query = query.filter(tour_schema.c.tourName.like((f'%{searchRq.searchParam}%')))


        total_count = await session.execute(query.with_only_columns(func.count().label('total')))
        total = total_count.scalar()

        hasMore = True if page*perPage < total else False

        paginated_query = query.limit(perPage).offset((page - 1) * perPage)
        result = await session.execute(paginated_query)
        res_list = result.mappings().all()
        list_of_tours = photosOptimization(res_list)
        return {
            "status": "success",
            "data": list_of_tours,
            "details": {
                "page": page,
                "perPage": perPage,
                "hasMore": hasMore
            }
        }

    # except:
    #     raise HTTPException(500, detail={
    #         "status": "ERROR",
    #         "data": None,
    #         "details": "Exception while trying to get tours from database"
    #     })

@router.get("/{id}", response_model=TourResponse)
async def tourDetails(id: str, session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        stmt = tour_schema.join(tours_plan, tour_schema.c.tourId == tours_plan.c.schemaId).join(User, tour_schema.c.ownerGidId == User.id)
        query = stmt.select().with_only_columns(tours_plan.c.id.label('publicTourId'), User.name.label('creatorName'), tour_schema.c.tourName, tours_plan.c.price,
                                                tour_schema.c.region, tour_schema.c.category,
                                                tour_schema.c.photos, tours_plan.c.dateFrom,
                                                tours_plan.c.dateTo, tours_plan.c.meetingPoint,
                                                tours_plan.c.meetingDatetime, tours_plan.c.maxPersonNumber, tour_schema.c.complexity,
                                                tour_schema.c.mapPoints, tour_schema.c.tourDescription,
                                                tour_schema.c.freeServices, tour_schema.c.additionalServices,
                                                tour_schema.c.recommendedAgeFrom, tour_schema.c.recommendedAgeTo
                                                ).where(tours_plan.c.id == id)
        result = await session.execute(query)
        res_dict = dict(result.mappings().first())

        query = offers.select()\
            .with_only_columns(func.sum(offers.c.touristsAmount).label('total')) \
            .filter(offers.c.tourPlanId == res_dict["publicTourId"])
        result = await session.execute(query)
        result = result.scalar()
        res_dict["vacancies"] = res_dict["maxPersonNumber"] - result


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

@router.post("/claim/create")
async def createClaim(claim: claimRq, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = insert(claims).values(
                touristId = user.id,
                publicTourId = claim.publicTourId,
                gidEmail = claim.gidEmail,
                description = claim.description,
                type="claim"
            )
        await session.execute(query)
        tourStateQuery = update(tours_plan).where(tours_plan.c.id == claim.publicTourId).values(state="consideration")
        await session.execute(tourStateQuery)
        await session.commit()
    except:
        raise HTTPException(500, detail={
            "status":"Error",
            "data":None,
            "details":"Error while creating a claim"
        })
    return {
        "status":"success",
        "data":None,
        "details":None
    }

@router.post("/appeal/create")
async def createClaim(description: str = Body(...), user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = insert(claims).values(
                touristId = user.id,
                description = description,
                type="appeal"
            )
        await session.execute(query)
        await session.commit()
    except:
        raise HTTPException(500, detail={
            "status":"Error",
            "data":None,
            "details":"Error while creating a claim"
        })
    return {
        "status":"success",
        "data":None,
        "details":None
    }

@router.post("/quest")
def questionToCreator(quest: questRq, user=Depends(current_user)):
    #do nothing
    return {
        "status":"success",
        "data":None,
        "details":None
    }