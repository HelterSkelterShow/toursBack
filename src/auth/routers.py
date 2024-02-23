from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import update
from src.auth.base_config import current_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.auth.schemas import innCheckRs
import datetime
import requests

from src.database import get_async_session

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/{inn}}", response_model=innCheckRs)
async def innValidate(inn:str, session : AsyncSession = Depends(get_async_session)) -> dict:
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
    return {"status": status}