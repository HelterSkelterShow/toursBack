import json
import uuid

from sqlalchemy import select, func, update

from src.admin.models import claims
from src.admin.schemas import UserListRs
from src.auth.base_config import current_user
from src.config import TOURISTS_PER_PAGE, CLAIMS_PER_PAGE
from src.creatorTours.models import offers, tours_plan

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from src.auth.models import User
from src.creatorTours.utils import photosOptimization
from src.database import get_async_session

router = APIRouter(
    prefix = "/admin/users",
    tags=["admin"]
)

router_claims = APIRouter(
    prefix = "/admin/claims",
    tags=["admin"]
)

router_appeals = APIRouter(
    prefix = "/admin/appeals",
    tags=["admin"]
)

@router.get("/list", response_model=UserListRs)
async def getAllUsers(emailString:str, page: int,  user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = select(User).where(User.email.like(f'%{emailString}%')).with_only_columns(User.id, User.name, User.email, User.phone, User.role_id, User.is_active)

        total_count = await session.execute(query.with_only_columns(func.count().label('total')))
        total = total_count.scalar()

        hasMore = True if page * TOURISTS_PER_PAGE < total else False

        paginated_query = query.limit(TOURISTS_PER_PAGE).offset((page - 1) * TOURISTS_PER_PAGE)
        result = await session.execute(paginated_query)
        res_list = result.mappings().all()
        list_of_users = [dict(row) for row in res_list]
    except:
        raise HTTPException(500, detail={
            "status":"Error",
            "data":None,
            "details":"Error while getting users from database"
        })
    return {
        "status": "success",
        "data": list_of_users,
        "details": {
            "page": page,
            "perPage": TOURISTS_PER_PAGE,
            "hasMore": hasMore
        }
    }


@router.post("/block/{id}")
async def blockUser(id: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = update(User).where(User.id == id).values(isActive = False)
        await session.execute(query)
        await session.commit()
    except:
        raise HTTPException(500, detail={
            "status":"Error",
            "data":None,
            "details":"Error while blocking user"
        })
    return {
        "status":"success",
        "data":id,
        "details":"user blocked"
    }

@router.post("/unblock/{id}")
async def unblockUser(id: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = update(User).where(User.id == id).values(isActive = True)
        await session.execute(query)
        await session.commit()
    except:
        raise HTTPException(500, detail={
            "status":"Error",
            "data":None,
            "details":"Error while unblocking user"
        })
    return {
        "status":"success",
        "data":id,
        "details":"user blocked"
    }

@router_claims.get("/list")
async def getClaimList(page: int,  user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        stmt = claims.join(User, claims.c.touristId == User.id)
        query = stmt.select().where((claims.c.state == "consideration") & (claims.c.type == "claim"))\
            .with_only_columns(User.email.label("touristEmail"), claims.c.claimId,
                               claims.c.gidEmail, claims.c.description,
                               claims.c.publicTourId, claims.c.state,
                               claims.c.creationDateTime)
        total_count = await session.execute(query.with_only_columns(func.count().label('total')))
        total = total_count.scalar()

        hasMore = True if page * CLAIMS_PER_PAGE < total else False

        paginated_query = query.limit(CLAIMS_PER_PAGE).offset((page - 1) * CLAIMS_PER_PAGE)
        result = await session.execute(paginated_query)
        res_list = result.mappings().all()
        list_of_claims = [dict(row) for row in res_list]
    except:
        raise HTTPException(500, detail={
            "status": "Error",
            "data": None,
            "details": "Error while getting users from database"
    })
    return {
        "status": "success",
        "data": list_of_claims,
        "details": {
            "page": page,
            "perPage": TOURISTS_PER_PAGE,
            "hasMore": hasMore
        }
    }

@router_claims.post("/confirm")
async def confirmClaim(calimId: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        stmt = select(claims).where(claims.c.claimId == calimId)
        claim = await session.execute(stmt)
        claim = dict(claim.mappings().first())
        query = update(claims).where(claims.c.claimId == calimId).values(state="confirmed")
        await session.execute(query)
        query_tours_plan = update(tours_plan).where(tours_plan.c.id == claim["publicTourId"]).values(state="refund")
        await session.execute(query_tours_plan)
        await session.commit()
    except:
        raise HTTPException(500, detail={
            "status":"Error",
            "data":None,
            "details":"Error while changing status"
        })
    return {
        "status":"success",
        "data":None,
        "details":None
    }

@router_claims.post("/reject")
async def rejectClaim(calimId: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        stmt = select(claims).where(claims.c.claimId == calimId)
        claim = await session.execute(stmt)
        claim = dict(claim.mappings().first())
        query = update(claims).where(claims.c.claimId == calimId).values(state="rejected")
        await session.execute(query)
        query_tours_plan = update(tours_plan).where(tours_plan.c.id == claim["publicTourId"]).values(state="isActive")
        await session.execute(query_tours_plan)
        await session.commit()
    except:
        raise HTTPException(500, detail={
            "status": "Error",
            "data": None,
            "details": "Error while changing status"
        })
    return {
        "status": "success",
        "data": None,
        "details": None
    }

@router_appeals.get("/list")
async def getAppeals(page: int,  user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        stmt = claims.join(User, claims.c.touristId == User.id)
        query = stmt.select().where((claims.c.state == "consideration") & (claims.c.type == "appeal"))\
            .with_only_columns(User.email.label("touristEmail"), claims.c.claimId,
                               claims.c.description,
                               claims.c.creationDateTime)
        total_count = await session.execute(query.with_only_columns(func.count().label('total')))
        total = total_count.scalar()

        hasMore = True if page * CLAIMS_PER_PAGE < total else False

        paginated_query = query.limit(CLAIMS_PER_PAGE).offset((page - 1) * CLAIMS_PER_PAGE)
        result = await session.execute(paginated_query)
        res_list = result.mappings().all()
        list_of_claims = [dict(row) for row in res_list]
    except:
        raise HTTPException(500, detail={
            "status": "Error",
            "data": None,
            "details": "Error while getting users from database"
    })
    return {
        "status": "success",
        "data": list_of_claims,
        "details": {
            "page": page,
            "perPage": TOURISTS_PER_PAGE,
            "hasMore": hasMore
        }
    }

@router_appeals.post("/confirm")
async def confirmAppeal(calimId: int, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = update(claims).where(claims.c.claimId == calimId).values(state="confirmed")
        await session.execute(query)
        await session.commit()
    except:
        raise HTTPException(500, detail={
            "status":"Error",
            "data":None,
            "details":"Error while changing status"
        })
    return {
        "status":"success",
        "data":None,
        "details":None
    }


