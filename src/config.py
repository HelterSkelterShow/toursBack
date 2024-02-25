from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

SECRET_AUTH = os.environ.get('SECRET')
RESET_AND_VERIFICATION = os.environ.get('RESET_AND_VERIFICATION_SECRET')

SESSION_LIFETIME = 3600

SMTP_USER=os.environ.get('SMTP_USER')
SMTP_PASSWORD=os.environ.get('SMTP_PASSWORD')

AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION=os.environ.get('AWS_DEFAULT_REGION')