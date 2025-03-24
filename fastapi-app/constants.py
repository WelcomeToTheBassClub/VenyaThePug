"""Константы"""
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import URL

from .configs import db_config

DB_URL = URL.create(
    "postgresql",
    username=db_config.user,
    password=db_config.password,
    host=db_config.host,
    database=db_config.db_name,
    port=db_config.port
)

CONNECT_PARAMS = {}

AUTH_SCHEME = OAuth2PasswordBearer(tokenUrl="token")

PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")
