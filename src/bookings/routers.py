import datetime
import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from select import select
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from src.auth.base_config import current_user
from src.auth.models import User
from src.bookings.schemas import BookingRq, bookedTour, Contact, Tour, bookings
from src.config import TOURIST_TIME_TO_CANCEL
from src.creatorTours.models import offers, tour_schema, tours_plan
from src.database import get_async_session

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"]
)

@router.post("/create")
async def createBooking(booking: BookingRq, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    if user.role_id != 1:
        raise HTTPException(403, detail={
            "status": "ACCESS ERROR",
            "data": None,
            "details": "Booking is available only for tourists"
        })
    try:
        tourists_json = json.dumps([{'name': t.name, 'birthDate': t.birthDate.isoformat()} for t in booking.tourists], ensure_ascii=False)
        tourists_json.replace("\\", "")
        query = insert(offers).values(
            id = uuid.uuid4(),
            tourPlanId = booking.publicTourId,
            tourAmount = booking.tourAmount,
            tourists = tourists_json,
            comment = booking.comment,
            touristId = user.id
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

@router.post("/list")
async def getMyBookings(isFinished: bool, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    if user.role_id != 1:
        raise HTTPException(403, detail={
            "status": "ACCESS ERROR",
            "data": None,
            "details": "Booking is available only for tourists"
        })
    try:
        stmt = offers.join(User, User.id == offers.c.touristId).join(tours_plan, tours_plan.c.id == offers.c.tourPlanId) \
            .join(tour_schema, tours_plan.c.schemaId == tour_schema.c.tourId)

        query = stmt.select().with_only_columns(tours_plan.c.state.label('statusBooking'), tours_plan.c.id.label('publicTourId'),
                                                tour_schema.c.tourName, tours_plan.c.price.label('tourAmount'),
                                                tours_plan.c.meetingPoint,
                                                tours_plan.c.meetingDatetime.label('meetingTime'),
                                                tours_plan.c.dateFrom,
                                                tours_plan.c.dateTo, tours_plan.c.state, User.email, User.phone,
                                                User.name, offers.c.id, tour_schema.c.mapPoints,
                                                tour_schema.c.additionalServices, tour_schema.c.freeServices, tour_schema.c.tourId) \
            .filter(User.id == user.id)
        if isFinished:
            query = query.filter(tours_plan.c.dateTo <= datetime.datetime.utcnow())
        else:
            query = query.filter(tours_plan.c.dateTo > datetime.datetime.utcnow())

        result = await session.execute(query)
        result = result.mappings().all()

        list_of_dicts = [bookedTour(
            statusBooking=row["statusBooking"],
            dateFrom=row['dateFrom'].isoformat(),
            dateTo=row['dateTo'].isoformat(),
            publicTourId=row['publicTourId'],
            bookingId=row['id'],
            cancelDeadline = row["dateFrom"] - datetime.timedelta(days=TOURIST_TIME_TO_CANCEL),
            tourAmount=row['tourAmount'],
            contactInformation=Contact(
                name=row['name'],
                email=row['email'],
                phone=row['phone']
            ),
            meetingPoint=row['meetingPoint'],
            meetingTime=row['meetingTime'].isoformat(),
            tour=Tour(
                tourId=(row['tourId']),
                tourName=row['tourName'],
                additionalServices=row['additionalServices'],
                freeServices=row['freeServices'],
                mapPoints=row['mapPoints']
            )
        ) for row in result]
    except:
        raise HTTPException(500, detail={
            "status":"DB_ERROR",
            "data":None,
            "details":"Error while inserting tour template into database"
        })
    return {
        "status": "success",
        "data": list_of_dicts,
        "details": None
    }

@router.post("/{id}")
async def cancelBooking(id: uuid.UUID, user = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = update(offers)\
            .where((offers.c.touristId == user.id) & (offers.c.id == id)).\
            values(cancellation=True)

        await session.execute(query)
        await session.commit()
    except:
        raise HTTPException(404, detail={
            "status":"Error",
            "data":None,
            "details":"No tour publication to cancel"
        })

    return {
        "status": "success",
        "data": id,
        "details": None
    }



# @router.get("")
# async def getBooking(session: AsyncSession = Depends(get_async_session)):
#     stmt = offers
#     query = stmt.select()
#     result = await session.execute(query)
#     res_list = result.mappings().all()
#     list_of_dicts = [dict(row) for row in res_list]
#     for offer in list_of_dicts:
#         offer["tourists"] = json.loads(offer["tourists"])
#     return {
#         "status": "success",
#         "data": list_of_dicts,
#         "details": None
#     }

