# app/db/scan.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.scan import ScanRecord
from bson import ObjectId

async def get_user_scans(user_id: str, db: AsyncIOMotorDatabase) -> list[ScanRecord]:
    cursor = db["scans"].find({"user_id": user_id}).sort("timestamp", -1)
    return [ScanRecord(**doc) async for doc in cursor]

async def get_all_scans(db: AsyncIOMotorDatabase) -> list[ScanRecord]:
    cursor = db["scans"].find().sort("timestamp", -1)
    return [ScanRecord(**doc) async for doc in cursor]

async def get_scan_by_id(scan_id: str, db: AsyncIOMotorDatabase) -> dict | None:
    try:
        oid = ObjectId(scan_id)
    except Exception:
        return None
    return await db["scans"].find_one({"_id": oid})
