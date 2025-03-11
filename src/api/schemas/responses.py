from src.schemas.base import BaseScheme
from src.schemas.auth import TokenInfo
from src.schemas.location import LocationScheme, LocationStatus


class Tokens(BaseScheme):
    access_token: TokenInfo
    refresh_token: TokenInfo


class Distance(BaseScheme):
    distance: float
    unit: str


class CheckDistanceResponse(BaseScheme):
    status: LocationStatus
    location: LocationScheme | None = None
    distance: Distance
