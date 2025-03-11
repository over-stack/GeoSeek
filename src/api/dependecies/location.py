from fastapi import Depends, HTTPException, status

from src.services.location import LocationService
from src.schemas.location import LocationScheme, LocationStatus
from src.db.repositories.location import LocationRepository
from src.api.dependecies.dbs import get_redis_client
from redis import asyncio as aioredis


def get_location_repository(rdb: aioredis.Redis = Depends(get_redis_client)):
    return LocationRepository(rdb)


def get_location_service(
    location_repo: LocationRepository = Depends(get_location_repository),
):
    return LocationService(location_repo)
