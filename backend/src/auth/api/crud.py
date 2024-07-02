from fastapi import Response
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from .schemas import UserCreateSchema
from auth.jwt_service import jwt_service
from auth.auth_service import auth_service
from .utils import create_jwt_and_set_cookie


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
