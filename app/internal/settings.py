from pydantic_settings import BaseSettings

from os import environ
from dotenv import load_dotenv

load_dotenv('.env')

GMAIL_SMTP_URL = environ.get('GMAIL_SMTP_URL')
GMAIL_SMTP_PORT = environ.get('GMAIL_SMTP_PORT')
GMAIL_USER = environ.get('GMAIL_USER')
GMAIL_APP_PWD = environ.get('GMAIL_APP_PWD')
API_TOKEN=environ.get('API_TOKEN')

class Settings(BaseSettings):
    gmail_smtp_url: str = GMAIL_SMTP_URL
    gmail_smtp_port: int = GMAIL_SMTP_PORT
    gmail_user: str = GMAIL_USER
    gmail_app_pwd: str = GMAIL_APP_PWD


settings = Settings()

versions_to_persist = 5

