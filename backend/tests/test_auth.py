from httpx import AsyncClient
from contextlib import nullcontext as does_not_raise

import pytest
from sqlalchemy.exc import IntegrityError


@pytest.mark.parametrize(
    ["user", "status_code"],
    [
        (
            {
                "username": "awsx",
                "email": "awsx@gmail.com",
                "password": "awsx123",
            },
            201,
        ),
        (
            {
                "username": "awsx",
                "email": "awsx@gmail.com",
                "password": "awsx123",
            },
            401,
        ),
        (
            {
                "username": "qwertyqwertyqwertyqwertyqwertyqwert",
                "email": "awsx@gmail.com",
                "password": "awsx123",
            },
            422,
        ),
    ],
)
async def test_register(ac: AsyncClient, user, status_code):
    response = await ac.post(
        "/auth/register",
        json=user,
    )
    assert response.status_code == status_code, response
    if status_code == 422:
        assert response.json()["detail"][0]["type"] == "string_too_long", response.json()
    if status_code == 401:
        assert response.json()["detail"] == f"Пользователь {user.get("username")} уже существует!", response.json()


async def test_login(ac: AsyncClient):
    response = await ac.post(
        "/auth/login", json={"username": "awsx", "password": "awsx123"}
    )
    assert response.status_code == 200, response


async def test_private_route(ac: AsyncClient):
    response = await ac.get("/auth/private_route")
    assert response.status_code == 200


async def test_get_payload(ac: AsyncClient):
    response = await ac.get("/auth/payload")
    assert response.status_code == 200
