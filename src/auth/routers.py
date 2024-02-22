from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import update
from src.auth.base_config import current_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
import datetime
import requests

from src.database import get_async_session

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/{inn}")
async def innValidate(inn:str, user: User = Depends(current_user), session : AsyncSession = Depends(get_async_session)) -> dict:
    date = datetime.date.today()
    date_str = date.isoformat()
    url = "https://statusnpd.nalog.ru/api/v1/tracker/taxpayer_status"
    data = {
        "inn": inn,
        "requestDate": date_str,
    }
    try:
        resp = requests.post(url=url, json=data, timeout=60)
        status = resp.json()["status"]
    except:
        raise HTTPException(500, detail={
            "status": "ERROR",
            "data": None,
            "details": "FNS_SERVICE_ERROR"
        })
    if resp.status_code != 200:
        raise HTTPException(500, detail={
            "status" : "ERROR",
            "data":None,
            "details":"FNS_SERVICE_ERROR"
        })
    try:
        if (status==True):
            stmt = update(User).where(User.id == user.id).values(inn_verification=status)
            await session.execute(stmt)
            await session.commit()
    except:
        raise HTTPException(500, detail={
            "status": "SERVER ERROR",
            "data": None,
            "details": "DB SAVE ERROR"
        })
    return {"status":status}