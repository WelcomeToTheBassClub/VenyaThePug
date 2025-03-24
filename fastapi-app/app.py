"""Application"""
from fastapi import FastAPI

from .models import Token, UserPublic, TransactionCreate, TransactionPublic, TransactionUpdate
from .auth import TokenDep, UserDep
from .db import SessionDep, save_transaction, update_transaction, delete_transaction

app = FastAPI()


@app.post("/token")
async def login(
    token: TokenDep
) -> Token:
    return token


@app.get("/users/me/", response_model=UserPublic)
async def read_users_me(
    current_user: UserDep
):
    return current_user


@app.post("/transactions/", response_model=TransactionPublic)
def publish_transaction(
        transaction: TransactionCreate,
        current_user: UserDep,
        session: SessionDep
):
    return save_transaction(current_user, transaction, session)


@app.post("/transactions/{transaction_id}", response_model=TransactionPublic)
def edit_transaction(
        transaction_id: int,
        transaction: TransactionUpdate,
        current_user: UserDep,
        session: SessionDep
):
    return update_transaction(transaction_id, transaction, current_user, session)


@app.delete("/transactions/{transaction_id}")
def drop_transaction(
        transaction_id: int,
        current_user: UserDep,
        session: SessionDep
):
    return delete_transaction(transaction_id, session)
