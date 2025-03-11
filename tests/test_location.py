import pytest
from httpx import AsyncClient
from src.config import settings


@pytest.mark.asyncio
async def test_generate_location(client: AsyncClient):
    response = await client.post(
        f"{settings.api_v1_prefix}/locations/generate",
        json={"latitude": 40.7128, "longitude": -74.0060},
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Location generated"}


@pytest.mark.asyncio
async def test_check_distance(client: AsyncClient):
    response = await client.get(
        f"{settings.api_v1_prefix}/locations/check-distance",
        params={"lat": 40.7128, "lon": -74.0060},
    )
    assert response.status_code == 200
    assert "distance" in response.json()
    assert "status" in response.json()
