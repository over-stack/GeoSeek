from src.schemas.base import BaseScheme
from src.schemas.auth import TokenInfo


class Tokens(BaseScheme):
    access_token: TokenInfo
    refresh_token: TokenInfo


class Distance(BaseScheme):
    distance: float
    unit: str
