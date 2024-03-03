import uuid

from fastapi import HTTPException
from sqlalchemy import select

from src.config import MAX_FILE_SIZE, MAX_FILE_SUM_SIZE, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID
from src.tours.models import tour_schema

from src.database import get_async_session

import boto3

def fileValidation(tourPhotos):
    fileSumSize = 0
    for tempFile in tourPhotos:
        if tempFile.content_type not in ("image/jpeg", "image/png"):
            raise HTTPException(400, detail={
                "status":"ERROR",
                "data":None,
                "details":"Разрешены только файлы форматов .png и .jpeg"
            })
        if tempFile.size//1024//1024 > MAX_FILE_SIZE:
            raise HTTPException(400, detail={
                "status": "ERROR",
                "data": None,
                "details": f"Максимальный размер файла {MAX_FILE_SIZE}Мб"
            })
        fileSumSize += tempFile.size//1024//1024 + 1
        if fileSumSize > MAX_FILE_SUM_SIZE:
            raise HTTPException(400, detail={
                "status": "ERROR",
                "data": None,
                "details": f"Максимальная сумма файлов {MAX_FILE_SUM_SIZE}Мб"
            })

def photosOptimization(res_list):
    list_of_dicts = [dict(row) for row in res_list]
    for tour in list_of_dicts:
        tour["photos"] = tour["photos"][0]
    return list_of_dicts


