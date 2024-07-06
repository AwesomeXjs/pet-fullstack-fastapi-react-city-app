from fastapi import Response

from src.db.models.user import User
from .exceptions import unauth_401_exc
from src.app_config import app_settings
from src.auth.jwt_service import jwt_service
from src.auth.api.schemas import UserCreateSchema

# создаем jwt и кладем его в куки
async def create_jwt_and_set_cookie(
    response: Response,
    username: str,
):
    access_token = jwt_service.create_jwt(
        token_data={
            "username": username,
        },
        expire_minutes=app_settings.jwt_settings.access_token_expire_minutes,
    )
    response.set_cookie(jwt_service.COOKIE_ALIAS, access_token)


# смотрим валидна ли кука, и удаляем ее
async def delete_cookie(payload: dict, response: Response):
    username = payload.get("username")
    if username is None:
        response.delete_cookie(jwt_service.COOKIE_ALIAS)
        raise unauth_401_exc(detail=f"Ваша сессия уже истекла!")
    response.delete_cookie(jwt_service.COOKIE_ALIAS)
    return {
        "Status": "OK",
        "data": f"До свидания, {username}!",
    }


# сверяет юзера в jwt и юзера в бд и делает апдейт
def validate_user_by_username(payload: dict, user: UserCreateSchema) -> bool:
    username_from_payload = payload.get("username")
    if username_from_payload is None:
        raise unauth_401_exc(f"Юзер в токене не найден")
    if user.username == username_from_payload:
        return True
    raise unauth_401_exc(f"Такой юзер не найден.")
