from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import router as v1_router
from src.app_config import app_settings
from src.auth.api.view import router as auth_router


app = FastAPI(title="Welcome to City!")
app.include_router(auth_router, tags=["Authorization and register"])
app.include_router(v1_router)


origins = [
    "https://awesomexjs.github.io",
    "https://awesomexjs.github.io/pet-fullstack-fastapi-react-city-app"
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:10000/",
    "http://localhost:8080",
    "https://aweso0mex.github.io/tech-magazine",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "OPTIONS",
        "DELETE",
        "PATCH",
        "PUT",
    ],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
