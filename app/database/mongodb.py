from motor.motor_asyncio import AsyncIOMotorClient

from app.config.settings import settings

client: AsyncIOMotorClient | None = None
database = None

def get_documents_collection():
    return database.documents

async def connect_to_mongo():
    global client, database

    client = AsyncIOMotorClient(settings.MONGODB_URI)
    database = client[settings.DATABASE_NAME]

    print("✅ Connected to MongoDB")


async def close_mongo_connection():
    global client

    if client:
        client.close()
        print("🔴 MongoDB connection closed")