import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from select import select
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.auth.models import User
from src.bookings.schemas import BookingRq
from src.creatorTours.models import offers
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
#
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

