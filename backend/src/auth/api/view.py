from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    status,
    Depends,
    Response,
    APIRouter,
)

from . import crud
from src.dependencies.session_dep import session_dependency
from .schemas import (
    UserSchema,
    UserCreateSchema,
    UserRegisterSchema,
)
from src.dependencies.auth_dep import (
    auth_by_jwt_payload,
    get_payload_from_jwt_cookie,
    login_user_by_username_and_password,
)
from src.db.models import User
from .utils import create_jwt_and_set_cookie

router = APIRouter(prefix="/auth")


@router.post(
    "/register",
    response_model=UserCreateSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    session: Annotated[
        AsyncSession,
        Depends(session_dependency),
    ],
    responce: Response,
    data: UserRegisterSchema,
) -> UserCreateSchema:
    return await crud.create_user(
        # response=responce,
        session=session,
        data=data,
    )


# Логин пользователя
@router.post(
    "/login",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    # response: Response,
    user: Annotated[
        UserCreateSchema,
        Depends(login_user_by_username_and_password),
    ],
):
    # await create_jwt_and_set_cookie(
    #     response=response,
    #     username=user.username,
    # )
    return UserSchema(id=user.id, username=user.username)


# Логаут (удаление кук)
@router.post(
    "/logout",
    # response_model=LogoutSchema,
    status_code=status.HTTP_200_OK,
)
async def logout_user(
    ## ЗАКОМЕНТИЛ СПЕЦИАЛЬНО ЧТОБЫ НА RENDER НОРМАЛЬНО РАБОТАЛ ЛОГАУТ ТАК КАК НЕ ГОНЯЮТСЯ КУКИ И ТОКЕНА ТАМ НЕТ
    # response: Response,
    # payload: Annotated[
    #     dict,
    #     Depends(get_payload_from_jwt_cookie),
    # ],
):
    return True
    # return await delete_cookie(
    #     response=response,
    #     payload=payload,
    # )


# Удаление пользователя
@router.post("/delete")
async def delete_user(
    # response: Response,
    username: str,
    # payload: Annotated[dict, Depends(get_payload_from_jwt_cookie)],
    session: Annotated[AsyncSession, Depends(session_dependency)],
):
    return await crud.delete_user(
        username=username,
        # response=response,
        # payload=payload,
        session=session,
    )


# проверка на валидность при переходе в другой роут ( проверка кук на юзернейм)
# @router.get("/private_route")
# async def auth_for_private_route(
#     username_from_payload: Annotated[
#         str,
#         Depends(auth_by_jwt_payload),
#     ],
# ) -> str:
#     return username_from_payload


# @router.get("/payload")
# async def get_payload(payload: Annotated[dict, Depends(get_payload_from_jwt_cookie)]):
#     return payload


@router.patch("/update")
async def update_user_password(
    response: Response,
    new_password: str,
    session: Annotated[AsyncSession, Depends(session_dependency)],
    user: User = Depends(login_user_by_username_and_password),
) -> UserCreateSchema:

    return await crud.update_password(
        response=response,
        session=session,
        user=user,
        new_password=new_password,
    )
