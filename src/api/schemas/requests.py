from src.schemas.base import BaseScheme
from pydantic import Field, SecretStr


class UserRegister(BaseScheme):
    username: str = Field(
        ..., min_length=3, max_length=50, pattern=r"^[a-z][a-z0-9_]*$"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        pattern=r"^[A-Za-z\d@$!%*?&]+$",
    )


class GenLocationRequest(BaseScheme):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
