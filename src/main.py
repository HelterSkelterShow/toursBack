from fastapi import FastAPI, Body, Path, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.auth.base_config import current_user
from src.auth.models import User
#from src.auth.routers import router as router_auth
from fastapi import APIRouter
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate

from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.tours.routers import router as router_tours


app = FastAPI()

#app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

origins = [
    "https://toursback.onrender.com/"
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

#app.include_router(router_auth)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/users",
    tags=["auth"],
)

#вариант, где требуется верификация через подтверждение почты
#app.include_router(
#    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
#    prefix="/auth/jwt",
#    tags=["auth"],
#)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/users",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/users",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/users",
    tags=["auth"],
)

#этот роутер надо будет переписать для работы с ЛК Админа и профилями. Ожидавется get user/list, user/{id}/block, user/{id}/activate
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=False),
    prefix="/users",
    tags=["users"],
)

app.include_router(router_tours)

@app.get("/protected-route", response_model=UserRead)
def protected_route(user: User = Depends(current_user)) -> dict:
    return user