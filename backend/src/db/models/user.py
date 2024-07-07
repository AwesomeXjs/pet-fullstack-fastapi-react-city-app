from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base

if TYPE_CHECKING:
    from .todo import Todo


class User(Base):
    username: Mapped[str] = mapped_column(String(20), unique=True)
    hashed_password: Mapped[str]

    todos: Mapped[list["Todo"]] = relationship(back_populates="user")
