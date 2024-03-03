import uuid
from typing import List, Optional

import boto3
from fastapi import APIRouter, Depends, UploadFile, Form, File

from src.auth.base_config import current_user
from src.auth.models import User
from src.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

router = APIRouter(
    prefix="/files",
    tags=["files"]
)

@router.post("/upload")
def uploadPhotoToBecket(tourPhotos: List[UploadFile] | None = None, user: User = Depends(current_user)) -> dict:
    if not tourPhotos:
        return {
            "status": "success",
            "data": [],
            "details": "Фото успешно загружены в бакет"
        }
    else:
        client = boto3.client(service_name="s3",
                              endpoint_url='https://storage.yandexcloud.net',
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        photosPath = []
        for tempFile in tourPhotos:
            id = uuid.uuid4()
            url = f"https://storage.yandexcloud.net/mywaytours/{id}"
            client.upload_fileobj(tempFile.file, 'mywaytours', str(id))
            photosPath.append(url)
        return {
            "status":"success",
            "data":photosPath,
            "details":"Фото успешно загружены в бакет"
        }
