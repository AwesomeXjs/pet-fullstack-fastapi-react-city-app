from typing import TYPE_CHECKING
from datetime import datetime, UTC

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base

if TYPE_CHECKING:
    from .user import User


class Todo(Base):
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))

    user_username: Mapped[str] = mapped_column(ForeignKey("users.username"))

    user: Mapped["User"] = relationship(back_populates="todos")
