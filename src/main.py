from fastapi import FastAPI

from src.api.routers import user, location

app = FastAPI()

app.include_router(user.router)
app.include_router(location.router)
