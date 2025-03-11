from datetime import datetime
from typing import Any
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClientSession

from src.config import settings


class MongoDBAdapter:
    def __init__(self, uri, db_name, max_pool_size=100):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            uri, maxPoolSize=max_pool_size
        )
        self.db = self.client[db_name]

    async def start_session(self) -> AsyncIOMotorClientSession:
        return await self.client.start_session()

    async def end_session(self, session: AsyncIOMotorClientSession) -> None:
        await session.end_session()

    async def insert_one(
        self,
        collection_name,
        document,
        session: AsyncIOMotorClientSession,
    ) -> str:
        collection = self.db[collection_name]
        result = await collection.insert_one(document, session=session)
        return result.inserted_id

    async def find_one(
        self,
        collection_name,
        query,
        session: AsyncIOMotorClientSession,
    ) -> dict:
        collection = self.db[collection_name]
        document = await collection.find_one(query, session=session)
        return document

    async def update_one(
        self,
        collection_name,
        query,
        update,
        session: AsyncIOMotorClientSession,
    ) -> int:
        collection = self.db[collection_name]
        result = await collection.update_one(query, {"$set": update}, session=session)
        return result.modified_count

    async def delete_one(self, collection_name, query, session) -> int:
        collection = self.db[collection_name]
        result = await collection.delete_one(query, session=session)
        return result.deleted_count

    async def find(
        self,
        collection_name,
        query,
        session: AsyncIOMotorClientSession,
    ) -> list[dict]:
        collection = self.db[collection_name]
        cursor = collection.find(query, session=session)
        documents = []
        async for document in cursor:
            documents.append(document)
        return documents

    async def create_index(
        self,
        collection_name,
        field_name,
        session: AsyncIOMotorClientSession,
    ) -> None:
        collection = self.db[collection_name]
        await collection.create_index(field_name, session)

    async def get_paginated_items(
        self,
        collection_name: str,
        field_name: str,
        field_value: Any,
        page_size: int,
        order: int,
        session: AsyncIOMotorClientSession,
    ):
        collection = self.db[collection_name]
        query = {}
        if field_value:
            match order:
                case 1:
                    query[field_name] = {"$gt": field_value}
                case -1:
                    query[field_name] = {"$lt": field_value}
                case _:
                    raise ValueError("Invalid order value")
        cursor = (
            collection.find(query, session=session)
            .sort(field_name, order)
            .limit(page_size)
        )
        items = await cursor.to_list(length=page_size)
        return items


# adapter instance
mongodb = MongoDBAdapter(settings.creds.ME_CONFIG_MONGODB_URL, "geopeek")
