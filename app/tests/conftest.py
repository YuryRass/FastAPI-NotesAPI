import json
from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import Base, async_engine, async_session
from app.main import app as fastapi_app
from app.notes.model import Notes
from app.users.model import Users

settings = get_settings()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database() -> None:
    """Создание тестовой базы данных."""
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    notes = open_mock_json("notes")

    session: AsyncSession
    async with async_session() as session:
        for Model, values in [
            (Users, users),
            (Notes, notes),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="function")
async def ac() -> AsyncClient: # type: ignore
    """Асинхронный HTTP клиент."""
    async with AsyncClient(
        app=fastapi_app,
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def authenticated_ac() -> AsyncClient: # type: ignore
    """Асинхронный клиент, который прошел аутентификацию."""
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post(
            "/auth/login",
            json={
                "email": "test@test.com",
                "password": "test",
            },
        )
        assert ac.cookies[settings.COOKIE_KEY]
        yield ac


@pytest.fixture(scope="function")
async def true_content() -> str:
    """Вывод верного контента с точки зрения орфографии."""
    return "Привет, мир!"


@pytest.fixture(scope="function")
async def invalid_content() -> str:
    """Вывод неверного контента с точки зрения орфографии."""
    return "Здесь ашибки в славах"
