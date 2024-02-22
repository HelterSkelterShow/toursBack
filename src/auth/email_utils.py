import base64

import requests

def send_email_password_reset(name: str, email: str, token: str):
    base64_token = base64.b64encode(bytes(token, 'utf-8'))  # bytes

    url = 'https://api.smtp.bz/v1/smtp/send'

    headers = {
    'Authorization':'qUBr7vnKSQveIDTOLY3q3jaksJ1rl1JBKbTH'
    }

    response = requests.post(
        url,
        headers=headers,
        files= {('from', (None, 'info@mywaytours.ru')),('subject', (None, 'Смена пароля')),('to', (None, f'{email}')),('html', (None, f'<div><h1 style=color: #007bff;>Здравствуйте, {name}, для смены пароля перейдите по ссылке 😊</h1><a style = display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; href="http://localhost:3000/reset-password/{base64_token}">Сменить пароль</a></div>'))},
        timeout=30
    )
    print(response.status_code, response.content)

def send_email_verification(name: str, email: str, token: str):
    base64_token = base64.b64encode(bytes(token, 'utf-8'))  # bytes
#    base64_token = b.decode('utf-8')  # convert bytes to string

    url = 'https://api.smtp.bz/v1/smtp/send'

    headers = {
    'Authorization':'qUBr7vnKSQveIDTOLY3q3jaksJ1rl1JBKbTH'
    }

    response = requests.post(
        url,
        headers=headers,
        files= {('from', (None, 'info@mywaytours.ru')),('subject', (None, 'Подтверждение регистрации')),('to', (None, f'{email}')),('html', (None, f'<div><h1 style=color: #007bff;>Здравствуйте, {name}, для подтверждения регистрации перейдите по ссылке 😊</h1><a style = display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; href="http://localhost:3000/verify/{base64_token}">Подтвердить регистрацию</a></div>'))},
        timeout=30
    )
    print(response.status_code, response.content)