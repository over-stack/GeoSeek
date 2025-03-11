from redis import asyncio as aioredis

from src.schemas.location import LocationScheme


class LocationRepository:
    def __init__(self, rdb: aioredis.Redis):
        self.rdb = rdb

    async def store_location(self, user_id: int, location: LocationScheme) -> None:
        d = location.model_dump()
        d.update({"gen_at": str(d["gen_at"])})
        await self.rdb.hset(
            f"loc:{user_id}",
            mapping=d,
        )

    async def get_location(self, user_id: int) -> LocationScheme | None:
        loc = await self.rdb.hgetall(f"loc:{user_id}")
        if not loc:
            return None
        return LocationScheme(**loc)

    async def delete_location(self, user_id: int) -> None:
        await self.rdb.delete(f"loc:{user_id}")
