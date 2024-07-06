from fastapi import APIRouter

from app_config import app_settings


router = APIRouter(prefix=app_settings.api_prefix.v1_prefix)
