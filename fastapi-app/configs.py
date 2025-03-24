"""Конфиги"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="fastapi-app/.env", env_file_encoding="utf-8", extra="ignore"
    )


class AuthConfig(BaseConfig):
    key: str
    algorithm: str
    expire_minutes: int

    model_config = SettingsConfigDict(env_prefix="jwt_")


class DbConfig(BaseConfig):
    host: str
    port: str
    db_name: str
    user: str
    password: str

    model_config = SettingsConfigDict(env_prefix="pg_")


auth_config = AuthConfig()
db_config = DbConfig()
