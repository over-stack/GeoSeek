from datetime import datetime, timezone
from src.schemas.location import LocationScheme, LocationStatus
from src.db.repositories.location import LocationRepository

from src.utils.location import generate_random_point, haversine_distance
from src.config import settings


class LocationService:
    def __init__(self, location_repo: LocationRepository):
        self.location_repo = location_repo

    async def generate_location(self, user_id: int, location: LocationScheme) -> None:
        new_lat, new_lon = generate_random_point(
            location.latitude, location.longitude, settings.params.LOCATION_RADIUS
        )
        new_location = LocationScheme(
            latitude=new_lat,
            longitude=new_lon,
            gen_at=datetime.now(timezone.utc),
        )
        await self.location_repo.store_location(user_id, new_location)

    async def get_location(self, user_id: int) -> LocationScheme | None:
        return await self.location_repo.get_location(user_id)

    async def get_distance(
        self, location1: LocationScheme, location2: LocationScheme
    ) -> float:
        return haversine_distance(
            location1.latitude,
            location1.longitude,
            location2.latitude,
            location2.longitude,
        )

    async def complete_location(self, user_id: int, status: LocationStatus) -> None:
        await self.location_repo.delete_location(user_id)
