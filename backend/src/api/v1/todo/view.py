from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends

from src.db.models.todo import Todo
from src.dependencies.todo_dep import get_todo_by_id
from src.services.todo_service import todo_service, TodoService
from .schemas import ToDoCreateSchema, ToDoSchemaReturn, ToDoUpdateSchema, ToDoSchema

router = APIRouter(prefix="/todo", tags=["Todo"])


@router.post(
    "/create",
    response_model=ToDoSchemaReturn,
)
async def create_todo(
    todo: ToDoCreateSchema,
    todo_service: TodoService = Depends(todo_service),
):
    return await todo_service.create_todo(todo)


@router.get("/get_one")
async def get_one_todo_by_id(
    todo: Annotated[Todo, Depends(get_todo_by_id)],
):
    return todo


@router.get("/all_of_user")
async def get_todos_by_user(
    username: str,
    todo_service: TodoService = Depends(todo_service),
):
    return await todo_service.get_all_by_user(username=username)


@router.delete("/del")
async def delete_todo_by_id(
    id: UUID,
    todo_service: TodoService = Depends(todo_service),
):
    return await todo_service.delete_one_by_id(id=id)


@router.patch("/patch")
async def update_todo_by_id(
    updated_todo: ToDoUpdateSchema,
    todo_service: Annotated[TodoService, Depends(todo_service)],
    todo: Annotated[ToDoSchema, Depends(get_todo_by_id)],
):
    return await todo_service.update_one(todo=todo, new_todo=updated_todo)


@router.get("/all", response_model=list[ToDoSchema])
async def get_all_todos(
    todo_service: Annotated[TodoService, Depends(todo_service)],
):
    todos = await todo_service.get_all_todos()
    return [
        ToDoSchema(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            user_username=todo.user_username,
        )
        for todo in todos
    ]
