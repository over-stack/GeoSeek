from datetime import datetime
from enum import Enum
from .base import BaseScheme
from pydantic import Field


class LocationStatus(Enum):
    ONTHEWAY = "ONTHEWAY"
    SUCCESS = "SUCCESS"
    CANCELLED = "CANCELLED"
    FAILURE = "FAILURE"


class LocationRead(BaseScheme):
    _id: str | None = None
    start_lat: float = Field(..., ge=-90, le=90)
    start_lon: float = Field(..., ge=-180, le=180)
    end_lat: float = Field(..., ge=-90, le=90)
    end_lon: float = Field(..., ge=-180, le=180)
    start_timestamp: datetime
    end_timestamp: datetime | None = None
    line_distance: float
    user_distance: float | None = None
    status: LocationStatus
    track_lat: list[float]
    track_lon: list[float]


class LocationScheme(BaseScheme):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
