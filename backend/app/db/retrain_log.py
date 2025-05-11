# app/db/retrain_log.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.retrain_log import RetrainLog

async def log_retrain_event(db: AsyncIOMotorDatabase, log: RetrainLog):
    await db.retrain_logs.insert_one(log.dict())
