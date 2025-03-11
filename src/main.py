from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api.routers import user, location
from src.db.redis import redis_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(location.router)
