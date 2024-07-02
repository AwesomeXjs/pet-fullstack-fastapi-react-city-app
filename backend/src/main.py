from fastapi import FastAPI

from api import router as v1_router


app = FastAPI(title="Welcome to City!")
app.include_router(v1_router)
