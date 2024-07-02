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
        token_expire_minutes: int,
    ) -> None:
        self.TOKEN_TYPE_FIELD = TOKEN_TYPE_FIELD
        self.ACCESS_TOKEN_TYPE = ACCESS_TOKEN_TYPE
        self.PRIVATE_KEY = PRIVATE_KEY.read_text()
        self.PUBLIC_KEY = PUBLIC_KEY.read_text()
        self.ALGORITHM = ALGORITHM
        self.token_expire_minutes = token_expire_minutes

    def jwt_encode(
        self,
        payload: dict,
        expire_time_delta: timedelta | None = None,
    ) -> str:
        """creating a jwt token based on the necessary data (payload)
        and with the ability to set your own expiration time

        Args:
                payload (dict): information that we want to transfer to the backend during authentication
                expire_time_delta (timedelta | None, optional): expiration time, for example timedelta(day=1),
                                                                if not set, it will be the default time (1440 minutes)
        Returns:
                        str: JWT token
        """
        payload_copy = payload.copy()

        # устанавливаем срок экспирации токена
        # now - текущее время
        now = datetime.utcnow()
        if expire_time_delta:
            expire = now + expire_time_delta
        else:
            expire = now + timedelta(minutes=self.token_expire_minutes)
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

    async def create_jwt(
        self,
        token_type: str,
        token_data: dict,
        expire_timedelta: timedelta | None = None,
    ):
        jwt_payload = {
            self.TOKEN_TYPE_FIELD: token_type,
        }
        jwt_payload.update(token_data)
        return self.encode_jwt(
            payload=jwt_payload,
            expire_time_delta=expire_timedelta,
            expire_minutes=self.token_expire_minutes,
        )


jwt_service = JWT_Service(
    TOKEN_TYPE_FIELD="type",
    ACCESS_TOKEN_TYPE="access",
    PRIVATE_KEY=app_settings.jwt_settings.private_key_path,
    PUBLIC_KEY=app_settings.jwt_settings.public_key_path,
    ALGORITHM=app_settings.jwt_settings.algorithm,
    token_expire_minutes=1440,
)
