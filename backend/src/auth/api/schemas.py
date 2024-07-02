from pydantic import BaseModel, ConfigDict


class UserCreateSchema(BaseModel):
    username: str
    email: str

    model_config = ConfigDict()
