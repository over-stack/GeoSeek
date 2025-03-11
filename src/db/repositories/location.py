from datetime import datetime, timezone
from redis import asyncio as aioredis
from motor.motor_asyncio import AsyncIOMotorClientSession
from src.utils.location import (
    haversine_distance,
    optimize_path,
    kalman_filter,
    calc_path_distance,
)
from src.db.mongodb import mongodb
from src.schemas.location import LocationScheme, LocationStatus, LocationRead


class LocationRepository:
    def __init__(self, rdb: aioredis.Redis, mdb: AsyncIOMotorClientSession) -> None:
        self.rdb = rdb
        self.mdb = mdb

    async def get_location(self, user_id: int) -> LocationScheme | None:
        loc = await self.rdb.hgetall(f"loc:{user_id}")
        if not loc:
            return None
        return LocationScheme(lat=loc["lat"], lon=loc["lon"])

    async def init_location(
        self,
        user_id: int,
        start_location: LocationScheme,
        end_location: LocationScheme,
    ) -> None:
        loc = LocationRead(
            start_lat=start_location.lat,
            start_lon=start_location.lon,
            end_lat=end_location.lat,
            end_lon=end_location.lon,
            start_timestamp=datetime.now(timezone.utc),
            line_distance=haversine_distance(
                start_location.lat,
                start_location.lon,
                end_location.lat,
                end_location.lon,
            ),
            track_lat=[],
            track_lon=[],
            status=LocationStatus.ONTHEWAY.value,
        )
        location_id = await mongodb.insert_one(
            "location", loc.model_dump(exclude_unset=True), session=self.mdb
        )
        await self.rdb.hset(
            f"loc:{user_id}",
            mapping={
                "id": location_id,
                "lat": end_location.lat,
                "lon": end_location.lon,
            },
        )
        await self.rdb.lpush(
            f"track_lat:{user_id}",
            start_location.lat,
        )
        await self.rdb.lpush(
            f"track_lon:{user_id}",
            start_location.lon,
        )

    async def complete_location(
        self, user_id: int, status: LocationStatus
    ) -> LocationRead:
        await self.process_tracks(user_id)

        loc = await self.rdb.hgetall(f"loc:{user_id}")
        if not loc:
            raise ValueError("Location not found")

        # get track_lat, track_lon from mongo
        track = await mongodb.find(
            "location",
            {"_id": loc["id"]},
            {"track_lat": 1, "track_lon": 1},
            session=self.mdb,
        )

        track_lat = track["track_lat"]
        track_lon = track["track_lon"]

        user_distance = calc_path_distance(track_lat, track_lon)

        d = {
            "status": status.value,
            "end_timestamp": datetime.now(timezone.utc),
            "user_distance": user_distance,
        }
        await mongodb.update_one(
            "location",
            {"_id": loc["id"]},
            d,
            session=self.mdb,
        )

        result = await mongodb.find_one(
            "location",
            {"_id": loc["id"]},
            session=self.mdb,
        )
        result = LocationRead(**result)

        await self.rdb.delete(f"loc:{user_id}")

        return result

    async def track_location(self, user_id: int, location: LocationScheme) -> float:
        await self.rdb.lpush(
            f"track_lat:{user_id}",
            location.lat,
        )
        await self.rdb.lpush(
            f"track_lon:{user_id}",
            location.lon,
        )

        if await self.rdb.llen(f"track_lat:{user_id}") > 100:
            await self.process_tracks(user_id)

        loc = await self.rdb.hgetall(f"loc:{user_id}")
        if not loc:
            raise ValueError("Location not found")

        dist = haversine_distance(
            location.lat,
            location.lon,
            float(loc["lat"]),
            float(loc["lon"]),
        )

        return dist

    async def process_tracks(self, user_id: int) -> None:
        track_lat: list[float] = await self.rdb.lrange(f"track_lat:{user_id}", 0, -1)
        track_lon: list[float] = await self.rdb.lrange(f"track_lon:{user_id}", 0, -1)
        if not track_lat or not track_lon:
            raise ValueError("Track not found")

        track_lat, track_lon = kalman_filter(track_lat, track_lon)
        track_lat, track_lon = optimize_path(track_lat, track_lon)

        loc = await self.rdb.hgetall(f"loc:{user_id}")
        if not loc:
            raise ValueError("Location not found")

        # update append track_lat, track_lon to mongo track_lat, track_lon (values should be appended)
        await mongodb.update_one(
            "location",
            {"_id": loc["id"]},
            {
                "$push": {
                    "track_lat": {"$each": track_lat},
                    "track_lon": {"$each": track_lon},
                }
            },
            session=self.mdb,
        )

        await self.rdb.delete(f"track_lat:{user_id}")
        await self.rdb.delete(f"track_lon:{user_id}")

    async def get_location_history(
        self,
        last_timestamp: datetime | None,
        page_size: int,
    ) -> list[LocationRead]:
        result = await mongodb.get_paginated_items(
            "location",
            "end_timestamp",
            last_timestamp,
            page_size,
            session=self.mdb,
        )
        return [LocationRead.model_validate(r) for r in result]
