from datetime import datetime, timezone
from src.schemas.location import LocationScheme, LocationStatus, LocationRead
from src.db.repositories.location import LocationRepository

from src.utils.location import generate_random_point, haversine_distance
from src.config import settings


class LocationService:
    def __init__(self, location_repo: LocationRepository):
        self.location_repo = location_repo

    async def generate_location(self, user_id: int, location: LocationScheme) -> None:
        if await self.location_repo.get_location(user_id) is not None:
            raise ValueError("Location already exists")
        new_lat, new_lon = generate_random_point(
            location.lat, location.lon, settings.params.LOCATION_RADIUS
        )
        new_location = LocationScheme(
            lat=new_lat,
            lon=new_lon,
        )
        await self.location_repo.init_location(user_id, location, new_location)

    async def cancel_location(
        self, user_id: int, location: LocationScheme
    ) -> LocationRead:
        return await self.location_repo.complete_location(
            user_id,
            location,
            LocationStatus.CANCELLED,
        )

    async def track_location(
        self, user_id: int, location: LocationScheme
    ) -> tuple[LocationRead | None, float]:
        dist = self.location_repo.track_location(user_id, location)
        if dist > settings.params.LOCATION_EPS_M:
            return None, dist
        return (
            await self.location_repo.complete_location(
                user_id,
                LocationStatus.SUCCESS,
            ),
            dist,
        )

    async def get_location_history(self, user_id: int) -> list[LocationRead]:
        return await self.location_repo.get_location_history(user_id)
