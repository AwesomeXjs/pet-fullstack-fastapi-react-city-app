from httpx import AsyncClient


async def test_logout_user(ac: AsyncClient):
    response = await ac.delete("/auth/logout")
    assert response.status_code == 200
