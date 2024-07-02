from fastapi import Response

from auth.jwt_service import jwt_service


async def create_jwt_and_set_cookie(
    response: Response,
    username: str,
    email: str,
):
    access_token = await jwt_service.create_jwt(
        token_data={
            "username": username,
            "email": email,
        },
    )
    response.set_cookie(jwt_service.COOKIE_ALIAS, access_token)
