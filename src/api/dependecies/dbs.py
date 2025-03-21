from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import async_session_maker
from typing import AsyncGenerator
from src.db.redis import redis_service
from redis import asyncio as aioredis
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession
from src.db.mongodb import mongodb


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_redis_client() -> AsyncGenerator[aioredis.Redis, None]:
    client = redis_service.connection_pool.client()
    yield client
    await client.aclose()


async def get_mongo_session() -> AsyncGenerator[AsyncIOMotorClientSession, None]:
    async with mongodb.start_session() as session:
        yield session
        await mongodb.end_session(session)
