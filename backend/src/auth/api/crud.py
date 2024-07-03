from fastapi import Response
from sqlalchemy import insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from auth.auth_service import auth_service
from .utils import create_jwt_and_set_cookie, delete_cookie
from .schemas import UserCreateSchema, UserSchema, UserRegisterSchema
from .exceptions import (
    unauth_401_exc,
    not_accept_401_exc,
    already_exist_406_exc,
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
        raise already_exist_406_exc(f"Пользователь {data.username} уже существует!")
    except Exception:
        raise not_accept_401_exc(
            f"Что то пошло не так, проверьте подключение к интернету!"
        )


async def delete_user(
    payload: dict,
    user: User,
    session: AsyncSession,
    response: Response,
) -> UserSchema:
    try:
        username_from_payload = payload.get("username")
        if username_from_payload is None:
            raise unauth_401_exc(f"Юзер {username_from_payload} не найден")
        if user.username == username_from_payload:
            stmt = delete(User).where(User.username == username_from_payload)
            await session.execute(stmt)
            await delete_cookie(
                payload=payload,
                response=response,
            )
            await session.commit()
        return user
    except Exception:
        raise something_wrong_400_exc(
            f"Что то пошло не так! Проверьте подключение к сети!"
        )
