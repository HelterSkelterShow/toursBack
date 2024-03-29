from typing import Optional
from pydantic import BaseModel

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    phone: str
    name: str
    inn: Optional[str]
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: str
    phone: str
    name: str
    inn: Optional[str]
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    pass

class innCheckRs(BaseModel):
    status: bool

