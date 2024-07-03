import pytest
from httpx import AsyncClient
from sqlalchemy import insert, delete

from db.models.user import User
from tests.conftest import session_factory_test


@pytest.fixture
def user_data():
    user = {
        "username": "awsx",
        "email": "awsx@gmail.com",
        "password": "awsx5",
    }
    return user


@pytest.fixture
async def create_user_fixture():
    async with session_factory_test() as session:
        stmt = insert(User).values(
            username="awsx",
            email="awsx@gmail.com",
            hashed_password="awsx5",
        )
        await session.execute(stmt)
        await session.commit()
    yield


@pytest.fixture
async def delete_users_fixture():
    yield
    async with session_factory_test() as session:
        stmt = delete(User)
        await session.execute(stmt)
        await session.commit()


@pytest.fixture
async def create_user_fixture(ac: AsyncClient, user_data):
    create_users = await ac.post("/auth/register", json=user_data)
    yield
