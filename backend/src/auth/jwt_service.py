import jwt
from datetime import timedelta, datetime

from app_config import app_settings


class JWT_Service:
    def __init__(
        self,
        TOKEN_TYPE_FIELD: str,
        ACCESS_TOKEN_TYPE: str,
        PRIVATE_KEY: str,
        PUBLIC_KEY: str,
        ALGORITHM: str,
        COOKIE_ALIAS: str,
        token_expire_minutes: int,
    ) -> None:
        self.TOKEN_TYPE_FIELD = TOKEN_TYPE_FIELD
        self.ACCESS_TOKEN_TYPE = ACCESS_TOKEN_TYPE
        self.PRIVATE_KEY = PRIVATE_KEY.read_text()
        self.PUBLIC_KEY = PUBLIC_KEY.read_text()
        self.ALGORITHM = ALGORITHM
        self.token_expire_minutes = token_expire_minutes
        self.COOKIE_ALIAS = COOKIE_ALIAS

    def jwt_encode(
        self,
        payload: dict,
        expire_minutes: int,
        expire_time_delta: timedelta | None = None,
    ) -> str:
        payload_copy = payload.copy()
        now = datetime.utcnow()
        if expire_time_delta:
            expire = now + expire_time_delta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        payload_copy.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            payload_copy,
            key=self.PRIVATE_KEY,
            algorithm=self.ALGORITHM,
        )
        return encoded

    def decode_jwt(
        self,
        token: str | bytes,
    ):
        decoded = jwt.decode(
            token,
            self.PUBLIC_KEY,
            algorithms=[self.ALGORITHM],
        )
        return decoded

    def create_jwt(
        self,
        token_data: dict,
        expire_minutes: int,
        expire_timedelta: timedelta | None = None,
    ):
        jwt_payload = {
            self.TOKEN_TYPE_FIELD: self.ACCESS_TOKEN_TYPE,
        }
        jwt_payload.update(token_data)
        return self.jwt_encode(
            payload=jwt_payload,
            expire_time_delta=expire_timedelta,
            expire_minutes=expire_minutes,
        )


jwt_service = JWT_Service(
    TOKEN_TYPE_FIELD="type",
    ACCESS_TOKEN_TYPE="access",
    PRIVATE_KEY=app_settings.jwt_settings.private_key_path,
    PUBLIC_KEY=app_settings.jwt_settings.public_key_path,
    ALGORITHM=app_settings.jwt_settings.algorithm,
    token_expire_minutes=app_settings.jwt_settings.access_token_expire_minutes,
    COOKIE_ALIAS=app_settings.jwt_settings.cookie_alias,
)
