import os

from fastapi_users.db import MongoDBUserDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticCollection

from app.models.users import UserDB

client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.get_database("fast_db")
movies_collection: AgnosticCollection = db["movies"]
user_collection: AgnosticCollection = db["users"]

user_db = MongoDBUserDatabase(UserDB, user_collection)
