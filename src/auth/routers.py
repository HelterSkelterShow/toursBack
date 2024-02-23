from fastapi import APIRouter, HTTPException, Depends
from src.auth.schemas import innCheckRs
from src.config import SECRET_AUTH, SESSION_LIFETIME
import datetime
import requests

from src.database import get_async_session

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/{inn}", response_model=innCheckRs)
def innValidate(inn : str) -> dict:
    date = datetime.date.today()
    date_str = date.isoformat()
    url = "https://statusnpd.nalog.ru/api/v1/tracker/taxpayer_status"
    data = {
        "inn": inn,
        "requestDate": date_str,
    }
    try:
        resp = requests.post(url=url, json=data)
        status = resp.json()["status"]
        if (resp.status_code != 200):
            raise HTTPException(500, detail={
                "status": "ERROR_OR_LIMIT",
                "data": None,
                "details": "FNS_SERVICE_ERROR_OR_LIMIT"
        })
    except:
        raise HTTPException(500, detail={
            "status": "ERROR",
            "data": None,
            "details": "FNS_SERVICE_ERROR"
        })
    return {"status": status}