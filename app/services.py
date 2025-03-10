from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_db
from app.models import Item, MongoModel


class BaseMongoService:
    COLLECTION: str
    ENTITY: MongoModel

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db[self.COLLECTION]

    async def create(self, entity: MongoModel) -> MongoModel:
        result = await self.collection.insert_one(entity.model_dump())
        created_damage_report = await self.get(result.inserted_id)
        return created_damage_report

    async def get(self, entity_id: ObjectId) -> MongoModel:
        result = await self.collection.find_one({"_id": entity_id})
        return self.ENTITY.model_validate(result)

    async def update(self, entity_id: ObjectId, update_data: dict[str, Any]) -> None:
        result = await self.collection.update_one({"_id": entity_id}, {"$set": update_data})
        return result.matched_count

    async def delete(self, entity_id: ObjectId) -> None:
        result = await self.collection.delete_one({"_id": entity_id})
        return result.deleted_count

    async def list(self, entity_ids: list[ObjectId] | None = None) -> list[MongoModel]:
        query_expr = {}
        if entity_ids:
            query_expr = {"_id": {"$in": entity_ids}}
        results = await self.collection.find(query_expr).to_list(length=None)
        return [self.ENTITY.model_validate(result) for result in results]


class ItemService(BaseMongoService):
    COLLECTION = "items"
    ENTITY = Item


def get_item_service() -> ItemService:
    return ItemService(db=get_db())
