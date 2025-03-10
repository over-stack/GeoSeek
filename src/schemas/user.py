from .base import BaseScheme
from datetime import datetime


class UserRead(BaseScheme):
    id: int
    username: str
    hashed_password: str
    active: bool
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseScheme):
    username: str
    hashed_password: str
