from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient

import pytest
from sqlalchemy import NullPool, delete, insert, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from main import app
from src.db import db_settings
from src.db.models import Base
from src.auth import auth_service
from src.db.models.user import User
from src.db.models.todo import Todo
from src.dependencies.session_dep import session_dependency


DB_URL_TEST = db_settings.postgres_db_url_test
engine_test = create_async_engine(
    url=DB_URL_TEST,
    poolclass=NullPool,
    echo=True,
)
session_factory_test = async_sessionmaker(bind=engine_test)
print(DB_URL_TEST)


# session dependency
async def override_session_dep():
    async with session_factory_test() as session:
        yield session
        await session.close()


app.dependency_overrides[session_dependency] = override_session_dep


@pytest.fixture(scope="session", autouse=True)
async def create_tables():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with engine_test.begin() as conn:
    # await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
