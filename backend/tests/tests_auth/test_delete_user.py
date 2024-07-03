from httpx import AsyncClient

from db.models import User
from tests.conftest import check_item_in_db


async def test_delete_user(ac: AsyncClient, user_data, create_user_fixture):
    response = await ac.post(
        "/auth/delete",
        json={"username": user_data["username"], "password": user_data["password"]},
    )
    item = await check_item_in_db(model=User, username=user_data["username"])
    assert response.status_code == 200, response
    assert item == None


async def test_delete_unregistered_user(
    ac: AsyncClient, user_data, create_user_fixture
):
    response = await ac.post(
        "/auth/delete", json={"username": "Nick", "password": "1234535"}
    )
    assert response.status_code == 401, response
    assert response.json()["detail"] == "Пользователь Nick не зарегистрирован"
