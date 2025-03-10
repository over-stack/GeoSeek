from datetime import timedelta
from src.schemas.user import UserRead
from src.schemas.auth import TokenInfo, TokenType

from src.utils.auth import encode_jwt, decode_jwt, hash_password, check_password
from src.db.repositories.auth import AuthRepository
from src.config import settings


class AuthService:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    def issue_access_token(self, user: UserRead) -> TokenInfo:
        payload = {
            "sub": str(user.id),
            "username": user.username,
        }
        token = encode_jwt(
            payload,
            expire_minutes=settings.auth_jwt.access_token_expire_minutes,
            token_type=TokenType.ACCESS,
        )
        return TokenInfo(token=token)

    async def issue_refresh_token(self, user: UserRead) -> TokenInfo:
        payload = {
            "sub": str(user.id),
            "username": user.username,
        }
        token = encode_jwt(
            payload,
            expire_timedelta=timedelta(
                days=settings.auth_jwt.refresh_token_expire_days
            ),
            token_type=TokenType.REFRESH,
        )

        jti = decode_jwt(token)["jti"]
        self.auth_repo.store_refresh_token(user_id=user.id, jti=jti)

        return TokenInfo(token=token)

    async def validate_token(
        self, token: str, tokenType: TokenType | None = None
    ) -> dict:
        payload = decode_jwt(token)
        if tokenType is None:
            return payload

        if payload["type"] != tokenType.name:
            raise ValueError("Invalid token type")

        if payload["type"] == TokenType.REFRESH.name:
            if not await self.auth_repo.check_refresh_token(
                user_id=int(payload["sub"]), jti=payload["jti"]
            ):
                raise ValueError("Invalid token")
        return payload

    async def revoke_refresh_token(self, user_id: int, jti: str) -> None:
        self.auth_repo.delete_refresh_token(user_id, jti)

    def hash_password(self, password: str) -> bytes:
        return hash_password(password)

    def check_password(self, password: str, hashed_password: bytes) -> bool:
        return check_password(password, hashed_password)
