"""Основной DAO (Data Access Object)"""

from typing import Any

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session


class BaseDAO:
    """
    Основной DAO. Реализует основные CRUD-операции к модели
    """

    model = None

    @classmethod
    async def find_one_or_none(cls, **kwargs: Any) -> Any:
        """Осуществляет поиск записи."""
        session: AsyncSession
        async with async_session() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = await session.execute(stmt)
            return result.one_or_none()

    @classmethod
    async def find(cls, **kwargs: Any) -> Any:
        """Поиск всех записей из модели."""
        session: AsyncSession
        async with async_session() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = await session.execute(stmt)
            return result.all()

    @classmethod
    async def add(cls, **data: Any) -> Any:
        """Добавление записи в таблицу."""
        stmt = insert(cls.model).values(**data).returning(cls.model.__table__.columns)
        session: AsyncSession
        async with async_session() as session:
            result = await session.execute(stmt)
            await session.commit()
            return result.one()

    @classmethod
    async def delete_rec(cls, **kwargs: Any) -> Any:
        """Удаление записей по условию."""
        stmt = delete(cls.model).filter_by(**kwargs).returning(cls.model.id)

        session: AsyncSession
        async with async_session() as session:
            result = await session.execute(stmt)
            await session.commit()
            return result.all()
