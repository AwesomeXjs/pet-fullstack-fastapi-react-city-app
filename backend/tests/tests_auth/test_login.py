from httpx import AsyncClient

from src.db.models.user import User
from src.auth.auth_service import auth_service


async def test_login_user(
    ac: AsyncClient,
    create_item_in_db,
    get_item_by_filter,
    user_data,
):

    await create_item_in_db(
        User,
        username=user_data["username"],
        hashed_password=auth_service.hash_password(user_data["password"]),
    )

    response = await ac.post(
        "/auth/login",
        json=user_data,
    )

    user_from_db = await get_item_by_filter(User, username=user_data["username"])

    assert response.status_code == 200

    assert (
        auth_service.validate_pass(
            hashed_password=user_from_db.hashed_password, password=user_data["password"]
        )
        == True
    ), "Пароль при регистрации не прошел проверку"


async def test_login_not_exist(ac: AsyncClient, get_item_by_filter):
    fake_data = {
        "username": "does6 not exist",
        "password": "12345",
    }
    response = await ac.post(
        "/auth/login",
        json=fake_data,
    )

    user = await get_item_by_filter(User, username=fake_data["username"])

    assert user == None
    assert response.status_code == 401, response.json()
