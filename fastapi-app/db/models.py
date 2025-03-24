from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field, Column, text
from sqlmodel import Text, Float, Integer, SmallInteger, BigInteger, DateTime


class Transaction(SQLModel, table=True):
    """Модель описывающая таблицу Transaction"""
    __tablename__ = "Transaction"

    id: Optional[int] = Field(
        default=None,
        sa_column=Column("TransactionId", BigInteger, primary_key=True)
    )
    description: str = Field(
        sa_column=Column("Description", Text)
    )
    amount: float = Field(
        sa_column=Column("Amount", Float)
    )
    maker_id: int = Field(
        sa_column=Column("Maker", Integer)
    )
    publisher_id: int = Field(
        sa_column=Column("Publisher", Integer)
    )
    category_id: int = Field(
        sa_column=Column("Category", SmallInteger)
    )
    transaction_dt: datetime = Field(
        sa_column=Column("Dt", DateTime)
    )
    creation_dt: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            "СreationDt",
            DateTime,
            server_default=text("now()")
        )
    )
    source_id: Optional[int] = Field(
        default=0,
        sa_column=Column("Source", SmallInteger)
    )


class TransactionCreate(SQLModel):
    """Модель для создания транзакции"""
    description: str
    amount: float
    category_id: int
    transaction_dt: datetime


class TransactionUpdate(SQLModel):
    """Модель для обновления транзакции"""
    description: Optional[str] = None
    amount: Optional[float] = None
    category_id: Optional[int] = None
    transaction_dt: Optional[datetime] = None


class TransactionPublic(TransactionCreate):
    """Модель для чтения транзакции"""
    id: int
    maker_id: int


class User(SQLModel, table=True):
    """Модель описывающая таблицу User"""
    __tablename__ = "User"

    id: int = Field(
        sa_column=Column("UserId", Integer, primary_key=True)
    )
    name: str = Field(
        sa_column=Column("Name", Text)
    )
    passhash: str = Field(
        sa_column=Column("PassHash", Text)
    )


class UserPublic(SQLModel):
    """Модель для чтения пользователя"""
    id: int
    name: str
