from httpx import AsyncClient


from db.models import User
from tests.conftest import check_item_in_db

async def test_register(
    ac: AsyncClient,
    delete_users_fixture,
    user_data,
):
    response = await ac.post(
        "/auth/register",
        json=user_data,
    )
    item = await check_item_in_db(model=User, username=user_data["username"])
    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"], response.json()
    assert item.username == user_data["username"]


async def test_register_again(
    ac: AsyncClient,
    user_data,
    delete_users_fixture,
    create_user_fixture,
):

    resonse = await ac.post(
        "/auth/register",
        json=user_data,
    )
    
    assert resonse.status_code == 406
    assert resonse.json()["detail"] == f"Пользователь {user_data["username"]} уже существует!"

