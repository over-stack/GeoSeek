from enum import Enum

from .base import BaseScheme


class TokenInfo(BaseScheme):
    token: str
    type: str = "Bearer"


class TokenType(Enum):
    ACCESS = 0
    REFRESH = 1
    EMAIL = 2


class TokenPair(BaseScheme):
    access_token: TokenInfo
    refresh_token: TokenInfo
