"""Модели"""
from pydantic import BaseModel

from .db.models import User, UserPublic, Transaction, TransactionCreate, TransactionPublic, TransactionUpdate


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
