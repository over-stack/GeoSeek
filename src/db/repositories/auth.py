from redis import asyncio as aioredis

from src.config import settings
from src.config import main_logger


class AuthRepository:
    def __init__(self, rdb: aioredis.Redis):
        self.rdb = rdb

    async def store_refresh_token(self, user_id: int, jti: str) -> None:
        await self.rdb.set(
            f"refresh:{user_id}:{jti}",
            "",
            settings.auth_jwt.refresh_token_expire_days * 24 * 60 * 60,
        )

    async def check_refresh_token(self, user_id: int, jti: str) -> bool:
        return await self.rdb.exists(f"refresh:{user_id}:{jti}")

    async def delete_refresh_token(self, user_id: int, jti: str) -> None:
        await self.rdb.delete(f"refresh:{user_id}:{jti}")
