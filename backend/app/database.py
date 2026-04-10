from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGODB_URL, DATABASE_NAME

_client = None
_db = None


async def connect_db():
    global _client, _db
    _client = AsyncIOMotorClient(MONGODB_URL)
    _db = _client[DATABASE_NAME]
    return _db


def close_db():
    global _client
    if _client:
        _client.close()


def get_db():
    return _db
