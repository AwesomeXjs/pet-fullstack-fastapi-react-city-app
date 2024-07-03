from httpx import AsyncClient


async def test_get_payload(ac: AsyncClient, delete_users_fixture, user_data):
    create_users = await ac.post("/auth/register", json=user_data)
    response = await ac.get("/auth/payload")
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]
