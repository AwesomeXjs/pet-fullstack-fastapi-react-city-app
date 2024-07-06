FROM python:latest

WORKDIR /app

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFED 1

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry install 

COPY . .

RUN alembic upgrade head && cd src

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

