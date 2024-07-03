from typing import Annotated

from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
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
from .exceptions import not_accept_406_exc, something_wrong_400_exc
from dependencies.auth_dep import (
    auth_by_jwt_payload,
    get_payload_from_jwt_cookie,
    login_user_by_username_and_password,
)
from .utils import create_jwt_and_set_cookie, delete_cookie

router = APIRouter(prefix="/auth")


@router.post(
    "/register",
    response_model=UserCreateSchema,
    status_code=status.HTTP_202_ACCEPTED,
)

# Регистрация нового пользователя
async def register_user(
    session: Annotated[AsyncSession, Depends(session_dependency)],
    responce: Response,
    username: Annotated[str, Form(max_length=20)],
    email: Annotated[EmailStr, Form(min_length=5)],
    password: Annotated[str, Form(min_length=5)],
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
        raise not_accept_406_exc(f"Пользователь {username} уже существует!")
    except Exception:
        raise not_accept_406_exc(
            f"Что то пошло не так, проверьте подключение к интернету!"
        )


# Логин пользователя
@router.post("/login")
async def login_user(
    response: Response,
    user: Annotated[
        UserCreateSchema,
        Depends(login_user_by_username_and_password),
    ],
) -> UserCreateSchema:
    create_jwt_and_set_cookie(
        response=response,
        email=user.email,
        username=user.username,
    )
    return user


# Логаут (удаление кук)
@router.delete("/logout")
async def logout_user(
    response: Response,
    payload: Annotated[
        dict,
        Depends(get_payload_from_jwt_cookie),
    ],
):
    return await delete_cookie(
        response=response,
        payload=payload,
    )


# Удаление пользователя
@router.delete("/delete")
async def delete_user(
    response: Response,
    user: Annotated[
        UserCreateSchema,
        Depends(login_user_by_username_and_password),
    ],
    payload: Annotated[dict, Depends(get_payload_from_jwt_cookie)],
    session: Annotated[AsyncSession, Depends(session_dependency)],
):
    try:
        delete_username = await crud.delete_user(
            response=response,
            user=user,
            payload=payload,
            session=session,
        )
        return delete_username
    except Exception:
        raise something_wrong_400_exc(
            f"Что то пошло не так! Проверьте подключение к сети!"
        )


# проверка на валидность при переходе в другой роут ( проверка кук на юзернейм)
@router.get("/private_route")
async def auth_for_private_route(
    validate_route: Annotated[bool, Depends(auth_by_jwt_payload)],
) -> bool:
    return validate_route
