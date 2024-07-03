from fastapi import Response
from sqlalchemy import insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from .schemas import UserCreateSchema
from .exceptions import unauth_401_exc
from auth.auth_service import auth_service
from .utils import create_jwt_and_set_cookie, delete_cookie


async def create_user(
    response: Response,
    username: str,
    password: str,
    session: AsyncSession,
    email: str,
) -> UserCreateSchema:
    hashed_password = auth_service.hash_password(password)
    stmt = insert(User).values(
        username=username,
        hashed_password=hashed_password,
        email=email,
    )
    await session.execute(stmt)
    create_jwt_and_set_cookie(
        response=response,
        email=email,
        username=username,
    )
    await session.commit()
    return UserCreateSchema(
        username=username,
        email=email,
    )


async def delete_user(
    payload: dict,
    user: User,
    session: AsyncSession,
    response: Response,
) -> str:
    username_from_payload = payload.get("username")
    if username_from_payload is None:
        raise unauth_401_exc(f"Юзер {username_from_payload} не найден")
    if user.username == username_from_payload:
        stmt = delete(User).where(User.username == username_from_payload)
        await session.execute(stmt)
        delete_cookie(payload=payload, response=response)
        await session.commit()
    return username_from_payload
