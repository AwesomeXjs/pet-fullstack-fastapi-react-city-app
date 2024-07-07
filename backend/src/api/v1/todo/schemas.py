from uuid import UUID
from datetime import datetime, UTC

from pydantic import BaseModel, Field, ConfigDict


class ToDoCreateSchema(BaseModel):
    user_username: str
    title: str = Field(max_length=20)
    description: str


class ToDoUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None


class ToDoDeleteSchema(BaseModel):
    title: str


class ToDoSchema(ToDoCreateSchema):
    id: UUID
    model_config = ConfigDict()


class ToDoSchemaReturn(ToDoCreateSchema):
    created_at: datetime
