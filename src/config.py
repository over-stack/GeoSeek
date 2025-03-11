import os
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Generator
from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import BaseModel, ConfigDict
import yaml

PROJECT_DIR: Path = Path(__file__).parent.parent.parent
BASE_DIR: Path = Path(__file__).parent.parent
STORAGE_DIR: Path = Path(__file__).parent.parent.parent / "storage"

with open(BASE_DIR / "config.yaml", "r") as file:
    config = yaml.safe_load(file)


class AppParams(BaseModel):
    LOCATION_RADIUS: float = config["LOCATION_RADIUS"]
    LOCATION_EPS_M: float = config["LOCATION_EPS_M"]


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    email_token_expire_minutes: int = 10


class Credentials(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    POSTGRES_DB: str

    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str

    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_PORT: int
    REDIS_DATABASES: int
    REDIS_DB: int

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    creds: Credentials = Credentials()
    params: AppParams = AppParams()

    api_v1_prefix: str = "/api/v1"

    @staticmethod
    def configure_logging(level: int = logging.INFO) -> None:
        if not os.path.exists("logs"):
            os.mkdir("logs")

        logging.basicConfig(
            level=level,
            datefmt="%Y-%m-%d %H:%M:%S",
            format="[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(lineno)d %(levelname)-8s - %(message)s",
            filename="logs/main_logger.log",
        )


settings = Settings()
settings.configure_logging()


main_logger = logging.getLogger("main_logger")
handler1 = logging.FileHandler("logs/main_logger.log")
handler1.setFormatter(
    logging.Formatter(
        fmt="[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(lineno)5d %(levelname)-8s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
main_logger.addHandler(handler1)
main_logger.setLevel(logging.INFO)
