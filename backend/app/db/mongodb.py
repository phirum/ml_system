# app/db/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Create MongoDB client and database handle
client = AsyncIOMotorClient(settings.DB_URI)
db = client["malware_analysis"]

# Dependency function for FastAPI
async def get_database():
    return db
