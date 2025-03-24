"""Модуль аутентификации"""
from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from .db import get_user, SessionDep
from .constants import AUTH_SCHEME
from .configs import auth_config
from .helpers import verify_password
from .models import TokenData, Token, User
from .exceptions import AUTH_ERROR, CREDENTIAL_ERROR


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Сгенерировать токен доступа

    Args:
        data:
        expires_delta:

    Returns:
        Токен доступа
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, auth_config.key, algorithm=auth_config.algorithm)

    return encoded_jwt


def authenticate_user(username: str, password: str, session: SessionDep) -> User | None:
    """Аутентификация пользователя

    Args:
        username: Никнейм
        password: Пароль
        session: Сессия

    Returns:
        Объект пользователя
    """
    user = get_user(username, session)

    if user and verify_password(password, user.passhash):
        return user

    return None


def get_jwt_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
) -> Token:
    """Получить токен аутентификации

    Args:
        form_data: Данные польхователя
        session: Сессия

    Returns:
        Токен
    """
    username = form_data.username
    password =form_data.password
    print(username, password)
    user = authenticate_user(username, password, session)

    if not user:
        raise AUTH_ERROR

    access_token_expires = timedelta(minutes=auth_config.expire_minutes)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


def get_current_user(
        token: Annotated[str, Depends(AUTH_SCHEME)],
        session: SessionDep
) -> User:
    """Получить авторизованного пользователя

    Args:
        token: Токен аутентификации
        session: Сессия

    Returns:

    """
    try:
        payload = jwt.decode(token, auth_config.key, algorithms=[auth_config.algorithm])
        username = payload.get("sub")

        if username is None:
            raise CREDENTIAL_ERROR

        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise CREDENTIAL_ERROR

    user = get_user(token_data.username, session)

    if user is None:
        raise CREDENTIAL_ERROR

    return user


UserDep = Annotated[User, Depends(get_current_user)]
TokenDep = Annotated[Token, Depends(get_jwt_token)]
