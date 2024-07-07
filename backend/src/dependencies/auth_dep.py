from typing import Annotated, Union

from sqlalchemy import select
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Cookie, Depends, Form, HTTPException

from src.db.models import User
from .session_dep import session_dependency
from src.auth.jwt_service import jwt_service
from src.auth.auth_service import auth_service
from src.auth.api.schemas import UserCreateSchema, UserLoginSchema
from src.auth.api.exceptions import unauth_401_exc, not_accept_406_exc


# возвращает данные из JWT токена из кук
async def get_payload_from_jwt_cookie(
    token: Annotated[Union[str, None], Cookie(alias=jwt_service.COOKIE_ALIAS)] = None,
) -> dict:
    if token is None:
        raise HTTPException(status_code=403, detail="No token provided")
    try:
        if isinstance(token, str):
            token = token.encode()
        payload = jwt_service.decode_jwt(token)
    except InvalidTokenError as e:
        return {"error": f"invalid token error: {e}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
    return payload


# Проверяет логин и пароль с бд и возвращает юзера
async def login_user_by_username_and_password(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    data: UserLoginSchema,
) -> User:
    query = select(User).filter_by(username=data.username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise unauth_401_exc(detail=f"Пользователь {data.username} не зарегистрирован")
    if not auth_service.validate_pass(
        password=data.password,
        hashed_password=user.hashed_password,
    ):
        raise unauth_401_exc(detail=f"Вы не правильно ввели пароль!")
    return user


# проверяет куки на юзернейм, если он там есть - возвращает True, либо выдает ошибку
async def auth_by_jwt_payload(
    payload: Annotated[dict, Depends(get_payload_from_jwt_cookie)],
) -> str:
    username = payload.get("username")
    if username is not None:
        return username

    raise not_accept_406_exc(
        f"Мы не смогли верифицировать вас, пожалуйста, зайдите в систему заного!"
    )
