from fastapi import Response

from app_config import app_settings
from .exceptions import unauth_401_exc
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
        expire_minutes=app_settings.jwt_settings.access_token_expire_minutes,
    )
    response.set_cookie(jwt_service.COOKIE_ALIAS, access_token)


# смотрим валидна ли кука, и удаляем ее
async def delete_cookie(payload: dict, response: Response):
    username = payload.get("username")
    if username is None:
        raise unauth_401_exc(detail=f"Ваша сессия уже истекла!")

    response.delete_cookie(jwt_service.COOKIE_ALIAS)
    return {
        "Status": "OK",
        "data": f"До свидания, {username}!",
    }
