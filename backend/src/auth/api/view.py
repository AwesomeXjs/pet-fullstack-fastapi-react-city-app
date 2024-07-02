from typing import Annotated

from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from .exceptions import unique_error, something_wrong

from fastapi import (
    Form,
    status,
    Depends,
    Response,
    APIRouter,
)

from . import crud
from .schemas import UserCreateSchema
from dependencies.session_dep import session_dependency

router = APIRouter(prefix="/auth")


@router.post(
    "/register",
    response_model=UserCreateSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def register_user(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    responce: Response,
    username: str = Form(max_length=20),
    email: EmailStr = Form(min_length=5),
    password: str = Form(min_length=5),
) -> UserCreateSchema:
    try:
        user = await crud.create_user(
            response=responce,
            session=session,
            username=username,
            email=email,
            password=password,
        )
        return user
    except IntegrityError as e:
        raise unique_error
    except Exception:
        raise something_wrong
