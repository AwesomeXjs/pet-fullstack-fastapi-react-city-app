from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


from ._base import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(20), unique=True)
    hashed_password: Mapped[str]
