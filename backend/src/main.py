import uvicorn

from fastapi import FastAPI

from api import router as v1_router
from app_config import app_settings
from auth.api.view import router as auth_router


app = FastAPI(title="Welcome to City!")
app.include_router(auth_router, tags=["Authorization and register"])
app.include_router(v1_router)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        port=app_settings.run_config.port,
        host=app_settings.run_config.host,
    )
