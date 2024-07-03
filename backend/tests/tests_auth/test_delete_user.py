from httpx import AsyncClient


async def test_delete_user(ac: AsyncClient, user_data):
    create_user_with_hashed_pass = await ac.post("/auth/register", json=user_data)
    response = await ac.post(
        "/auth/delete",
        json={"username": user_data["username"], "password": user_data["password"]},
    )
    assert response.status_code == 200, response


async def test_delete_unregistered_user(ac: AsyncClient, user_data):
    create_user_with_hashed_pass = await ac.post("/auth/register", json=user_data)
    response = await ac.post(
        "/auth/delete", json={"username": "Nick", "password": "1234535"}
    )
    assert response.status_code == 401, response
    assert response.json()["detail"] == "Пользователь Nick не зарегистрирован"
