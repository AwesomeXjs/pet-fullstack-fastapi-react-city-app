from typing import Annotated
from datetime import UTC, datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Todo
from src.dependencies.session_dep import session_dependency
from src.api.v1.todo.schemas import ToDoCreateSchema, ToDoSchema
from src.respositories import SQLAlchemyRepository, AbstractRepository


class TodoRepository(SQLAlchemyRepository):
    model = Todo


class TodoService:
    def __init__(
        self,
        repo,
        session,
    ):
        self.repo: AbstractRepository = repo(session)
        self.session = session

    # создать todo
    async def create_todo(
        self,
        todo: ToDoCreateSchema,
        created_at: datetime = datetime.fromisoformat(
            datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S")
        ),
    ):
        new_todo = todo.model_dump()
        new_todo.update(created_at=created_at)
        await self.repo.create_one(new_todo)
        await self.session.commit()
        return new_todo

    async def get_all_todos(self):
        return await self.repo.get_all()

    # найти todo по id
    async def get_one_todo(self, id: int):
        return await self.repo.get_one(id=id)

    # найти все todo конкретного пользователя
    async def get_all_by_user(
        self,
        username: str,
    ):
        todos = await self.repo.get_all_by_filter(user_username=username)
        return todos

    # удалить todo по id
    async def delete_one_by_id(
        self,
        id: int,
    ):
        todo_title = await self.repo.delete_one_by_id(id=id)
        await self.session.commit()
        return todo_title

    # обновить todo
    async def update_one(
        self,
        new_todo,
        todo: Todo,
    ):

        await self.repo.update_one(
            updated_item=new_todo,
            item=todo,
        )
        await self.session.commit()
        return {
            "old_data": todo,
            "new_data": ToDoSchema(
                title=new_todo.title,
                description=new_todo.description,
                id=todo.id,
                user_username=todo.user_username,
            ),
        }


def todo_service(session: Annotated[AsyncSession, Depends(session_dependency)]):
    return TodoService(repo=TodoRepository, session=session)
