from httpx import AsyncClient


async def test_register(
    ac: AsyncClient,
    delete_users_fixture,
    user_data,
):
    response = await ac.post(
        "/auth/register",
        json=user_data,
    )
    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"], response.json()


async def test_register_again(
    ac: AsyncClient,
    create_user_fixture,
    user_data,
    delete_users_fixture,
):
    response = await ac.post(
        "/auth/register",
        json=user_data,
    )
    assert response.status_code == 406
    assert response.json()["detail"] == f"Пользователь {user_data["username"]} уже существует!"

