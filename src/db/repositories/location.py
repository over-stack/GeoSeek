import redis.asyncio as aioredis

from src.schemas.location import LocationScheme


class LocationRepository:
    def __init__(self, rdb: aioredis.Redis):
        self.rdb = rdb

    async def store_location(self, user_id: int, location: LocationScheme) -> None:
        await self.rdb.hset(
            f"loc:{user_id}",
            mapping=location.model_dump(),
        )

        await self.rdb.expire(f"loc:{user_id}", 24 * 60 * 60)

    async def get_location(self, user_id: int) -> LocationScheme | None:
        loc = await self.rdb.hgetall(f"loc:{user_id}")
        if not loc:
            return None
        return LocationScheme(**loc)

    async def delete_location(self, user_id: int) -> None:
        await self.rdb.delete(f"loc:{user_id}")
