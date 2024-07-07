from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient

import pytest
from sqlalchemy import NullPool, delete, insert, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from main import app
from src.db import db_settings
from src.db.models import Base
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


##############################################
##############################################

##############################################
##############################################


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


##############################################
##############################################

##############################################
##############################################


@pytest.fixture()
def user_data():
    user = {
        "username": "awsx",
        "password": "awsx5",
    }
    return user


tables = [User, Todo]


# ОЧИСТКА ТАБЛИЦ ДО ТЕСТА И ПОСЛЕ ТЕСТА
@pytest.fixture(scope="function", autouse=True)
async def clean_tables():
    async with session_factory_test() as session:
        for table in tables:
            query = delete(table)
            await session.execute(query)
        await session.commit()
    yield
    async with session_factory_test() as session:
        for table in tables:
            query = delete(table)
            await session.execute(query)
        await session.commit()


# ПОИСК ИТЕМА ПО ID В БАЗЕ ДЛЯ ПРОВЕРКИ
@pytest.fixture
async def get_item_by_filter():

    async def get_item_from_db_by_uuid(model, **filter_by):
        async with session_factory_test() as session:
            query = select(model).filter_by(**filter_by)
            res = await session.execute(query)
            item = res.scalar_one_or_none()
            return item

    return get_item_from_db_by_uuid


# СОЗДАНИЕ ИТЕМА В БД ПЕРЕД ТЕСТОМ
@pytest.fixture
async def create_item_in_db():

    async def create_item(model, **values):
        async with session_factory_test() as session:
            stmt = insert(model).values(**values)
            await session.execute(stmt)
            await session.commit()

    return create_item
