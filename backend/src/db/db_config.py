from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


SRC_DIR = Path(__file__).parent.parent.parent

print(SRC_DIR)


class Db_Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASS: str
    DB_USER: str

    DB_NAME_TEST: str

    @property
    def postgres_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def postgres_db_url_test(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME_TEST}"

    model_config = SettingsConfigDict(env_file=SRC_DIR / ".env")


db_settings = Db_Settings()
