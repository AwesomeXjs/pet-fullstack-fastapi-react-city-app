from httpx import AsyncClient

async def test_login_not_register(ac: AsyncClient, user_data):
    response = await ac.post(
        "/auth/login",
        json={
            "username": user_data["username"],
            "password": user_data["password"],
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == f"Пользователь {user_data["username"]} не зарегистрирован"

