import os
from motor.motor_asyncio import AsyncIOMotorClient

from app.constants import DEFAULT_MONGODB_URI

class Database:
    DATABASE_NAME = "my_database"

    def __init__(self, uri: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[self.DATABASE_NAME]

def get_db():
    uri = os.getenv("MONGODB_URI", DEFAULT_MONGODB_URI)
    database = Database(uri)
    return database.db