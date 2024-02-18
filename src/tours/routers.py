from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.tours.models import tour_schema, tours_plan, offers
from src.auth.models import User
from src.database import get_async_session
from src.tours.schemas import TourSearchRq, RsList

router = APIRouter(
    prefix="/tours"
)

#@router.post("/search", response_model=List[RsList])
#def searchTours(filters:TourSearchRq, limit: int, offset: int, session : AsyncSession = Depends(get_async_session)):
#    try:
#        schema = aliased(tour_schema)
#        plan = aliased(tours_plan)
#        query = session.query(plan.id, schema.tourName, schema.photos, schema.category, schema.complexity, plan.price, schema.region, plan.dateFrom, plan.dateTo, plan.maxPersonNumber)\
#            .join(Order).all()
#        result = await session.execute(query)
#        return {"status":"success",
#                "data":result.all(),
#                "details":None
#                }
#    except:
#        raise HTTPException(500, detail={
#                "status" : "error",
#               "data":None,
#                "details":None
#                })