import smtplib

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import get_async_session

import smtplib
from email.message import EmailMessage

from src.config import SMTP_PASSWORD, SMTP_USER

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

def get_email_template_dashboard(username: str, e_mail: EmailStr, token):
    email = EmailMessage()
    email['Subject'] = 'Подтверждение регистрации'
    email['From'] = SMTP_USER
    email['To'] = e_mail

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Здравствуйте, {username}, подтвердите свою регистрацию на нашей прекрасной платформе 😊</h1>'
        '<a src="https://static.vecteezy.com/system/resources/previews/008/295/031/original/custom-relationship'
        '-management-dashboard-ui-design-template-suitable-designing-application-for-android-and-ios-clean-style-app'
        '-mobile-free-vector.jpg" width="600">'
        '</div>',
        subtype='html'
    )
    return email

def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)