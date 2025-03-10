from src.db.base import BaseORM, CREATED_AT, UPDATED_AT, str_256

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class User(BaseORM):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str_256] = mapped_column(unique=True)
    hashed_password: Mapped[str_256]
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[CREATED_AT]
    updated_at: Mapped[UPDATED_AT]
