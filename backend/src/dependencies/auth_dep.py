from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Cookie, Depends, Form, Responseonse

from db.models import User
from auth.jwt_service import jwt_service
from auth.auth_service import auth_service
from .session_dep import session_dependency
from jwt.exceptions import InvalidTokenError
from auth.api.schemas import UserCreateSchema
from auth.api.exceptions import unauth_401_exc, not_accept_406_excfrom auth.api.exceptions import unauth_401_exc, not_accept_406_exc


# возвращает данные из JWT токена из кук
async def get_payload_from_jwt_cookie(
    token: str = Cookie(alias=jwt_service.COOKIE_ALIAS),
) -> dict:
    try:
        payload = jwt_service.decode_jwt(token)
    except InvalidTokenError as e:
        return {"error": f"invalid token error: {e}"}
    return payload


# Проверяет логин и пароль с бд и возвращает юзера
async def login_user_by_username_and_password(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    username: Annotated[str, Form(max_length=20)],
    password: Annotated[str, Form(min_length=5)],
) -> UserCreateSchema:
    query = select(User).filter_by(username=username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise unauth_401_exc(detail=f"Пользователь {username} не зарегистрирован")
    if not auth_service.validate_pass(
        password=password,
        hashed_password=user.hashed_password,
    ):
        raise unauth_401_exc(detail=f"Вы не правильно ввели пароль!")
    return user


# проверяет куки на юзернейм, если он там есть - возвращает True, либо выдает ошибку
async def auth_by_jwt_payload(
    payload: Annotated[dict, Depends(get_payload_from_jwt_cookie)],
) -> bool:
    username = payload.get("username")
    if username is not None:
        return True

    raise not_accept_406_exc(
        f"Мы не смогли верифицировать вас, пожалуйста, зайдите в систему заного!"
    )

