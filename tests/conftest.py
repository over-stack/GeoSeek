from typing import AsyncGenerator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from redis import asyncio as aioredis

from src.main import app
from src.db.base import async_session_maker
from src.db.redis import redis_service


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(scope="function")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def redis_client() -> AsyncGenerator[aioredis.Redis, None]:
    client = redis_service.connection_pool.client()
    yield client
    await client.aclose()


# app.dependency_overrides[async_session_maker] = lambda: async_session
# app.dependency_overrides[redis_service.connection_pool.client] = lambda: redis_client
