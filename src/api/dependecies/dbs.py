from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import async_session_maker
from typing import AsyncGenerator
from src.db.redis import redis_service
from redis import asyncio as aioredis


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_redis_client() -> aioredis.Redis:
    return await redis_service.get_redis_client()
