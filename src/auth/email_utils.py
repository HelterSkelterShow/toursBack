import smtplib
from email.message import EmailMessage

import requests

from pydantic import EmailStr

from src.config import SMTP_PASSWORD, SMTP_USER

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def get_email_template_password_reset(user: str, e_mail: EmailStr, token):
    email = EmailMessage()
    email['Subject'] = 'Восстановление пароля'
    email['From'] = SMTP_USER
    email['To'] = e_mail

    email.set_content(
        '<div>'
        f'<h1 style="color: #007bff;">Здравствуйте, {user}, для смены пароля перейдите по ссылке 😊</h1>'
        '<a style = "display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;" href="https://domain.ru/api/change-password?token=qweqwe">Сменить пароль</a>'
        '</div>',
        subtype='html'
    )
    return email


def send_email_password_reset(user: str, email: str, token: str):
#    email = get_email_template_password_reset(user, email, token)
#    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
#        server.login(SMTP_USER, SMTP_PASSWORD)
#        server.send_message(email)
    url = 'https://api.smtp.bz/v1/smtp/send'
    headers = {
    'Authorization': 'qUBr7vnKSQveIDTOLY3q3jaksJ1rl1JBKbTH',
    'Content-Type': 'multipart/form-data'
    }
    data = {
        'from': 'r.sergey2001@ya.ru',
        'subject ': 'Восстановление пароля',
        'to': 'r.sergey2002@ya.ru',
        'html':'<div>'
        f'<h1 style="color: #007bff;">Здравствуйте, {user}, для смены пароля перейдите по ссылке 😊</h1>'
        '<a style = "display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;" href="https://domain.ru/api/change-password?token=qweqwe">Сменить пароль</a>'
        '</div>'
    }
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code, response.json())


def get_email_template_verification(username: str, e_mail: EmailStr, token):
    email = EmailMessage()
    email['Subject'] = 'Подтверждение регистрации'
    email['From'] = SMTP_USER
    email['To'] = e_mail

    email.set_content(
        '<div>'
        f'<h1 style="color: #007bff;">Здравствуйте, {username}, подтвердите свою регистрацию на нашей прекрасной платформе 😊</h1>'
        '<a style = "display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;" href="https://domain.ru/api/verify?token=qweqwe">Подтвердить</a>'
        '</div>',
        subtype='html'
    )
    return email

def send_email_verification(username: str, email: str, token: str):
    email = get_email_template_verification(username, email, token)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)