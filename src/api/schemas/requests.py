from src.schemas.base import BaseScheme


class UserRegister(BaseScheme):
    username: str
    password: str


class GenLocationRequest(BaseScheme):
    latitude: float
    longitude: float
