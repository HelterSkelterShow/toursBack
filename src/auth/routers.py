from fastapi import APIRouter
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate

from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate



