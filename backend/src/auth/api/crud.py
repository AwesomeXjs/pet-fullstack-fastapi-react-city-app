from fastapi import Response
from sqlalchemy import insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from auth.auth_service import auth_service
from .schemas import UserCreateSchema, UserSchema, UserRegisterSchema
from .utils import create_jwt_and_set_cookie, delete_cookie, validate_user_by_username
from .exceptions import (
    not_accept_406_exc,
    something_wrong_400_exc,
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
            email=data.email,
        )
        await session.execute(stmt)
        create_jwt_and_set_cookie(
            response=response,
            email=data.email,
            username=data.username,
        )
        await session.commit()
        return UserCreateSchema(
            username=data.username,
            email=data.email,
        )
    except IntegrityError as e:
        raise not_accept_406_exc(f"Пользователь {data.username} уже существует!")
    except Exception:
        raise something_wrong_400_exc(
            f"Что то пошло не так, проверьте подключение к интернету!"
        )


async def delete_user(
    payload: dict,
    user: UserCreateSchema,
    session: AsyncSession,
    response: Response,
) -> UserSchema:
    try:
        if validate_user_by_username(payload=payload, user=user):
            stmt = delete(User).where(User.username == payload.get("username"))
            await session.execute(stmt)
            await delete_cookie(
                payload=payload,
                response=response,
            )
            await session.commit()
        return user
    except Exception as e:
        raise something_wrong_400_exc(
            f"Что то пошло не так! Проверьте подключение к сети! {e}"
        )
