"""Вспомогательные функции"""
from .constants import PWD_CTX


def verify_password(plain_password, hashed_password):
    return PWD_CTX.verify(plain_password, hashed_password)


def get_password_hash(password):
    return PWD_CTX.hash(password)
