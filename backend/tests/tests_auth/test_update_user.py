from httpx import AsyncClient


async def test_update_user(
    ac: AsyncClient,
    user_data,
    delete_users_fixture,
):
    create_user = await ac.post("/auth/register", json=user_data)
    response = await ac.patch(
        "/auth/update",
        params={"new_username": "nickolay"},
        json={
            "username": user_data["username"],
            "password": user_data["password"],
        },
    )
    assert response.status_code == 200, response
