from datetime import datetime
from enum import Enum
from .base import BaseScheme


class LocationStatus(Enum):
    SUCCESS = 0
    CANCELLED = 1
    FAILURE = 2


class LocationScheme(BaseScheme):
    latitude: float
    longitude: float
    gen_at: datetime | None = None
