# from fastapi import Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.db.models.todo import Todo
from src.auth.auth_service import auth_service

# from src.auth.api.exceptions import unauth_401_exc
from .schemas import UserCreateSchema, UserRegisterSchema

# from .utils import create_jwt_and_set_cookie, delete_cookie, validate_user_by_username
from .exceptions import (
    not_accept_406_exc,
    user_already_find_202,
    something_wrong_400_exc,
)


async def create_user(
    # response: Response,
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
        # await create_jwt_and_set_cookie(
        #     response=response,
        #     username=data.username,
        # )
        await session.commit()
        return UserCreateSchema(
            username=data.username,
        )
    except IntegrityError as e:
        raise user_already_find_202(f"Пользователь {data.username} уже существует!")
    except Exception as e:
        raise something_wrong_400_exc(f"Что то пошло не так! Детали: {e}")


async def delete_user(
    # payload: dict,
    session: AsyncSession,
    # response: Response,
    username: str,
) -> UserCreateSchema | None:
    # if username != payload.get("username"):
    #     raise unauth_401_exc(f"Пользователь {username} не зарегистрирован")
    query = select(User).where(User.username == username)
    res = await session.execute(query)
    result = res.scalar_one_or_none()
    if result is None:
        raise not_accept_406_exc("Пользователь не найден")
    # if username == payload.get("username"):
    stmt = delete(User).where(User.username == username)
    await session.execute(stmt)
    # await delete_cookie(
    #     payload=payload,
    #     response=response,
    # )
    await session.commit()
    return UserCreateSchema(username=username)


# if payload.get("username") is None:
# raise not_accept_406_exc("Пожалуйста войдите в систему заного!")


async def update_password(
    # response: Response,
    session: AsyncSession,
    user: User,
    new_password: str,
):
    try:
        hashed_password = auth_service.hash_password(new_password)
        setattr(user, "hashed_password", hashed_password)

        # Ensure this part is correctly handled asynchronously
        # await create_jwt_and_set_cookie(
        #     response=response,
        #     username=user.username,
        # )

        await session.commit()
        return UserCreateSchema(username=user.username)
    except Exception as e:
        raise something_wrong_400_exc(f"Что-то пошло не так! Детали: {e}")
