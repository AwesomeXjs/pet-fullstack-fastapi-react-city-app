from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .db_config import db_settings


class DB_Helper:
    def __init__(
        self,
        url: str,
        echo: bool,
        pool_size: int,
    ) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=pool_size,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )


db_helper = DB_Helper(
    url=db_settings.postgres_db_url,
    echo=True,
    pool_size=50,
)
