from typing import Annotated

from sqlmodel import create_engine, Session
from fastapi import Depends

from ..constants import DB_URL, CONNECT_PARAMS


def get_session():
    with Session(engine) as session:
        yield session

engine = create_engine(DB_URL, connect_args=CONNECT_PARAMS, echo=True)
SessionDep = Annotated[Session, Depends(get_session)]
