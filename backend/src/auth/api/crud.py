from fastapi import Response
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from .schemas import UserCreateSchema
from auth.jwt_service import jwt_service
from auth.auth_service import auth_service


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
    access_token = await jwt_service.create_jwt(
        token_data={"username": username},
    )
    response.set_cookie(jwt_service.COOKIE_ALIAS, access_token)
    await session.commit()
    return UserCreateSchema(
        username=username,
        email=email,
    )
