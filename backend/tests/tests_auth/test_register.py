from httpx import AsyncClient

from src.db.models.user import User
from src.auth.auth_service import auth_service


async def test_register(
    ac: AsyncClient,
    user_data,
    get_item_by_filter,
):
    response = await ac.post(
        "/auth/register",
        json=user_data,
    )

    user_from_db = await get_item_by_filter(User, username=user_data["username"])

    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"], response.json()
    assert user_from_db != None, user_from_db
    assert user_from_db.username == user_data["username"], user_from_db.json()
    assert (
        auth_service.validate_pass(
            hashed_password=user_from_db.hashed_password, password=user_data["password"]
        )
        == True
    ), "Пароль при регистрации не прошел проверку"


async def test_register_already_exist(
    ac: AsyncClient,
    user_data,
    create_item_in_db,
):
    await create_item_in_db(
        User,
        username=user_data["username"],
        hashed_password=auth_service.hash_password(user_data["password"]),
    )
    response = await ac.post(
        "/auth/register",
        json=user_data,
    )

    assert response.status_code == 202
    assert response.json()["detail"] == "Пользователь awsx уже существует!"
