from datetime import datetime
import pika
import uvicorn
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from src.auth.base_config import auth_backend, fastapi_users

from src.auth.schemas import UserRead, UserCreate, UserUpdate
# from src.config import RABBIT_USERNAME, RABBIT_HOST, RABBIT_PORT, RABBIT_PASSWORD
from src.creatorTours.routers import router as router_tours
from src.auth.routers import router as router_users
from src.catalogs.routers import router as router_catalogs
from src.files.routers import router as router_files
from src.touristTours.routers import router as router_tourist
from src.bookings.routers import router as router_booking
from src.admin.routers import router as router_admin
from src.admin.routers import router_claims
from src.admin.routers import router_appeals


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

# scheduler = AsyncIOScheduler(timezone=utc)
# scheduler.add_job(printer, trigger=CronTrigger(hour='*', minute='*/1'))
# scheduler.start()

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

app.include_router(router_tourist)

app.include_router(router_booking)

app.include_router(router_admin)

app.include_router(router_claims)

app.include_router(router_appeals)

# @app.post("/sendToQueue")
# def sendToQueue():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT, credentials=pika.PlainCredentials(f'{RABBIT_USERNAME}', f'{RABBIT_PASSWORD}')))
#     channel = connection.channel()
#     channel.queue_declare(queue='hello')
#     channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
#     print(" [x] Sent 'Hello World!'")
#     connection.close()
#
# @app.post("/redFromQueue")
# def sendToQueue():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT, credentials=pika.PlainCredentials(f'{RABBIT_USERNAME}', f'{RABBIT_PASSWORD}')))
#     channel = connection.channel()
#     channel.queue_declare(queue='hello')
#     def callback(ch, method, properties, body):
#         print(" [x] Received %r" % body)
#     channel.basic_consume(callback, queue='hello', no_ack=True)
#     print(' [*] Waiting for messages, press CTRL+C to exit')
#     channel.start_consuming()