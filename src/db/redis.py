from redis import asyncio as aioredis

from src.config import settings, main_logger


class RedisConnector:
    def __init__(
        self,
        host: str,
        port: int,
        password: str | None,
        db: int = 0,
        max_connections: int = 10,
        socket_connect_timeout: float = 5,
        socket_timeout: float = 5,
        decode_responses: bool = True,
    ) -> None:
        self.config: dict = {
            "host": host,
            "port": port,
            "password": password,
            "db": db,
        }
        self.redis_url = (
            f"redis://{self.config["host"]}:{self.config["port"]}/{self.config["db"]}"
        )
        self.decode_responses: bool = decode_responses
        self.max_connections: int = max_connections
        self.socket_connect_timeout: float = socket_connect_timeout
        self.socket_timeout: float = socket_timeout
        self.connection_pool = aioredis.Redis(
            **self.config,
            socket_connect_timeout=self.socket_connect_timeout,
            socket_timeout=self.socket_timeout,
            max_connections=self.max_connections,
            decode_responses=self.decode_responses,
        )

    def get_connection_pool(self) -> aioredis.Redis:
        return self.connection_pool


redis_service = RedisConnector(
    host=settings.creds.REDIS_HOST,
    port=settings.creds.REDIS_PORT,
    password=settings.creds.REDIS_PASSWORD,
    db=settings.creds.REDIS_DB,
)
