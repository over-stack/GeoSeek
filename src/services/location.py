from datetime import datetime
from src.schemas.location import LocationScheme, LocationStatus
from src.db.repositories.location import LocationRepository

from src.utils.location import generate_random_point, haversine_distance


class LocationService:
    def __init__(self, location_repo: LocationRepository):
        self.location_repo = LocationRepository

    async def generate_location(self, user_id: int, location: LocationScheme) -> None:
        new_lat, new_lon = generate_random_point(location.latitude, location.longitude)
        new_location = LocationScheme(
            latitude=new_lat,
            longitude=new_lon,
            gen_at=datetime.now(datetime.timezone.utc),
        )
        await self.location_repo.store_location(user_id, new_location)

    async def get_location(self, user_id: int) -> LocationScheme:
        return await self.location_repo.get_location(user_id)

    async def get_distance(self, user_id: int, location: LocationScheme) -> float:
        loc = await self.location_repo.get_location(user_id)
        return haversine_distance(
            loc.latitude, loc.longitude, location.latitude, location.longitude
        )

    async def complete_location(self, user_id: int, status: LocationStatus) -> None:
        await self.location_repo.delete_location(user_id)
