# app/db/retrain_log.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.retrain_log import RetrainLog

async def log_retrain_event(db: AsyncIOMotorDatabase, log: RetrainLog) -> None:
    collection = db["retrain_logs"]
    await collection.insert_one(log.dict())

async def get_all_retrain_logs(db: AsyncIOMotorDatabase) -> list[RetrainLog]:
    collection = db["retrain_logs"]
    cursor = collection.find().sort("timestamp", -1)
    return [RetrainLog(**doc) async for doc in cursor]
