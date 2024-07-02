from fastapi import FastAPI

from api import router as v1_router
from auth.api.view import router as auth_router


app = FastAPI(title="Welcome to City!")
app.include_router(auth_router, tags=["Authorization and register"])
app.include_router(v1_router)
