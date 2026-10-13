
from pymongo import AsyncMongoClient

from app.config.settings import settings


client = AsyncMongoClient(settings.MONGODB_URL)
database = client[settings.DATABASE_NAME]

users_collection = database["users"]
tasks_collection = database["tasks"]



async def connect_to_mongodb():
    await client.admin.command("ping")

    await users_collection.create_index("email", unique=True)

    print("MongoDB Atlas connected successfully!")



async def close_mongodb_connection():
    await client.close()
