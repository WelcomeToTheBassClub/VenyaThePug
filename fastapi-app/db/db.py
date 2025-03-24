"""Модуль работы с БД"""
from datetime import datetime

from sqlmodel import select

from ..exceptions import NOT_FOUND_ERROR
from .models import Transaction, TransactionCreate, TransactionUpdate, User
from .engine import Session


def save_transaction(
        user: User,
        new_transaction: TransactionCreate,
        session: Session
) -> Transaction:
    """Сохранить транзакцию в БД

    Args:
        user: пользователь
        new_transaction: транзакция
        session: сессия

    Returns:
        Сохраненная транзакция
    """
    transaction = Transaction.model_validate(
        new_transaction,
        update={
            "maker_id": user.id,
            "publisher_id": user.id
        }
    )
    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    return transaction


def update_transaction(
        transaction_id: int,
        upd_transaction: TransactionUpdate,
        user: User,
        session: Session
) -> Transaction:
    """Обновить транзакцию в БД

    Args:
        transaction_id:
        upd_transaction:
        user:
        session:

    Returns:
        Обновлённая транзакция
    """
    transaction = session.get(Transaction, transaction_id)

    if not transaction:
        raise NOT_FOUND_ERROR

    update_data = upd_transaction.model_dump(exclude_unset=True)
    update_data["publisher_id"] = user.id
    update_data["creation_dt"] = datetime.now()

    transaction.sqlmodel_update(update_data)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    return transaction


def delete_transaction(
        transaction_id: int,
        session: Session
) -> dict:
    """Удалить транзакцию из БД

    Args:
        transaction_id:
        session:

    Returns:
         Результат удаления
    """
    transaction = session.get(Transaction, transaction_id)

    if not transaction:
        raise NOT_FOUND_ERROR

    session.delete(transaction)
    session.commit()

    return {"ok": True}


def get_user(username: str, session: Session) -> User | None:
    """Получает пользователя по никнейму

    Args:
        username: никнейм
        session: сессия

    Returns:
        Объект пользователя
    """
    query = session.exec(
        select(User).where(
            User.name == username
        )
    )
    return query.one_or_none()
