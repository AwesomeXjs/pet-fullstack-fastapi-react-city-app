import bcrypt


class AuthService:

    # хешируем пароль указаный при регистрации
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt).decode()

    # хешируем введенный пароль и сверяеми с хешем в базе данных
    def validate_pass(
        self,
        password: str,
        hashed_password: str,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password.encode(),
        )


auth_service = AuthService()
