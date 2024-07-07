from uuid import UUID
from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.db.models.todo import Todo
from src.services.todo_service import todo_service, TodoService


async def get_todo_by_id(
    id: UUID,
    todo_service: Annotated[TodoService, Depends(todo_service)],
) -> Todo:
    todo = await todo_service.get_one_todo(id=id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Такая тудушка не найдена",
        )
    return todo
