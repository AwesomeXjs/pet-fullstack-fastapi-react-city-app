from fastapi import Response
from sqlalchemy import insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from auth.auth_service import auth_service
from auth.api.exceptions import unauth_401_exc
from .schemas import UserCreateSchema, UserRegisterSchema
from .utils import create_jwt_and_set_cookie, delete_cookie, validate_user_by_username
from .exceptions import (
    not_accept_406_exc,
    something_wrong_400_exc,
    user_already_find_202,
)


async def create_user(
    response: Response,
    session: AsyncSession,
    data: UserRegisterSchema,
) -> UserCreateSchema:
    try:
        hashed_password = auth_service.hash_password(data.password)
        stmt = insert(User).values(
            username=data.username,
            hashed_password=hashed_password,
        )
        await session.execute(stmt)
        create_jwt_and_set_cookie(
            response=response,
            username=data.username,
        )
        await create_jwt_and_set_cookie(
            response=response,
            username=data.username,
        )
        await session.commit()
        return UserCreateSchema(
            username=data.username,
        )
    except IntegrityError as e:
        raise user_already_find_202(f"Пользователь {data.username} уже существует!")
    except Exception as e:
        raise something_wrong_400_exc(f"Что то пошло не так! Детали: {e}")


async def delete_user(
    payload: dict,
    session: AsyncSession,
    response: Response,
    username: str,
) -> UserCreateSchema | None:
    if username != payload.get("username"):
        raise unauth_401_exc(f"Пользователь {username} не зарегистрирован")
    try:
        if username == payload.get("username"):
            stmt = delete(User).where(User.username == payload.get("username"))
            await session.execute(stmt)
            await delete_cookie(
                payload=payload,
                response=response,
            )
            await session.commit()
            return UserCreateSchema(username=username)
        if payload.get("username") is None:
            raise not_accept_406_exc("Пожалуйста войдите в систему заного!")
    except Exception as e:
        raise something_wrong_400_exc(f"Что то пошло не так! Детали: {e}")


async def update_username(
    response: Response,
    session: AsyncSession,
    user: UserCreateSchema,
    new_username: str,
    payload: dict,
):
    try:
        if validate_user_by_username(
            payload=payload,
            user=user,
        ):
            setattr(
                user,
                "username",
                new_username,
            )
            create_jwt_and_set_cookie(
                response=response,
                username=new_username,
            )
            await session.commit()
            return user
    except Exception as e:
        raise something_wrong_400_exc(f"Что то пошло не так! Детали: {e}")
