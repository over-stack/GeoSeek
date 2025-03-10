from datetime import datetime

from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, create_engine, DateTime, func

from typing import Annotated, AsyncGenerator
from sqlalchemy.orm import mapped_column

from src.config import settings

async_engine = create_async_engine(
    settings.creds.DB_URL,
    echo=False,
)


async_session_maker = async_sessionmaker(
    async_engine,
    autoflush=False,
    expire_on_commit=False,
)


# SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

CREATED_AT = Annotated[
    datetime, mapped_column(DateTime(timezone=True), server_default=func.now())
]
UPDATED_AT = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    ),
]

str_256 = Annotated[str, 256]


class BaseORM(DeclarativeBase):
    __abstract__ = True

    type_annotation_map = {
        str_256: String(256),
    }

    repr_cols_num = 3
    repr_cols: tuple = tuple()

    def __repr__(self) -> str:
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class BaseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
