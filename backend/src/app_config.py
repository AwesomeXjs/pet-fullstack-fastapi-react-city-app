from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

KEYS_DIR = Path(__file__).parent / "auth" / "jwt_keys"


class JWT_Settings(BaseSettings):
    private_key_path: Path = KEYS_DIR / "jwt-private.pem"
    public_key_path: Path = KEYS_DIR / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 1  # 1 minute
    cookie_alias: str = "JWT-ACCESS-TOKEN"


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000


class ApiPrefixes(BaseModel):
    v1_prefix: str = "/v1"
    users_prefx: str = "/users"


class App_Settings(BaseSettings):
    run_config: RunConfig = RunConfig()
    api_prefix: ApiPrefixes = ApiPrefixes()
    jwt_settings: JWT_Settings = JWT_Settings()


app_settings = App_Settings()