import datetime
from typing import Optional
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    email: str
    phone: str
    createdAt: datetime.datetime
    role: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserCreate(schemas.BaseUserCreate):
    name: str
    email: str
    password: str
    phone: str
    createdAt: datetime.datetime
    role: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

