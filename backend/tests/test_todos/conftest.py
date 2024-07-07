import pytest


@pytest.fixture
def todo_data():
    todo = {
        "user_username": "awsx",
        "title": "string",
        "description": "string",
    }
    return todo
