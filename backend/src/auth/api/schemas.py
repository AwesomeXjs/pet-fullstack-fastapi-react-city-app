from pydantic import BaseModel, ConfigDict, Field


class UserCreateSchema(BaseModel):
    username: str = Field(max_length=20)
    email: str = Field(min_length=5)
    model_config = ConfigDict()


class UserRegisterSchema(UserCreateSchema):
    password: str = Field(min_length=5)


class UserLoginSchema(BaseModel):
    username: str = Field(max_length=20)
    password: str = Field(min_length=5)


class UserSchema(UserCreateSchema):
    id: int


class LogoutSchema(BaseModel):
    Status: str
    data: str
