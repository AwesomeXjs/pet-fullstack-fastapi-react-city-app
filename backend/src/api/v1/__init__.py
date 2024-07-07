from fastapi import APIRouter

from src.app_config import app_settings
from .todo.view import router as todo_router


router = APIRouter(prefix=app_settings.api_prefix.v1_prefix)
router.include_router(todo_router)
