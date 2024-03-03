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
from src.auth.routers import router as router_users
from src.catalogs.routers import router as router_catalogs
from src.files.routers import router as router_files


app = FastAPI()

origins = [
    "https://toursback.onrender.com/"
    "http://localhost",
    "http://localhost:8000",
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

app.include_router(router_users)

app.include_router(router_catalogs)

app.include_router(router_files)

@app.get("/protected-route", response_model=UserRead)
def protected_route(user: User = Depends(current_user)) -> dict:
    return user