from datetime import datetime
from enum import Enum
from .base import BaseScheme


class LocationStatus(Enum):
    ONTHEWAY = "ONTHEWAY"
    SUCCESS = "SUCCESS"
    CANCELLED = "CANCELLED"
    FAILURE = "FAILURE"


class LocationScheme(BaseScheme):
    latitude: float
    longitude: float
    gen_at: datetime | None = None
