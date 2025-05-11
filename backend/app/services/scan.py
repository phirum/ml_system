# app/services/scan.py
from datetime import datetime
from app.core.config import settings
from app.ml_engine.predictor import analyze_file
from app.models.scan import ScanRecord
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(settings.DB_URI)
db = client["malware_analysis"]
scans_collection = db["scans"]

async def process_scan(file_path: str, filename: str, user_id: str):
    result = analyze_file(file_path)
    
    scan_data = {
        "filename": filename,
        "user_id": user_id,
        "result": result["result"],
        "threat_type": result.get("threat_type"),
        "confidence": result["confidence"],
        "created_at": datetime.utcnow()
    }
    
    await scans_collection.insert_one(scan_data)
    return scan_data

# app/services/scan.py (extend existing file)
from bson import ObjectId

async def get_user_scans(user_id: str):
    scans = await scans_collection.find({"user_id": user_id}).to_list(length=100)
    return scans

async def get_all_scans():
    scans = await scans_collection.find().sort("created_at", -1).to_list(length=100)
    return scans

async def get_scan_by_id(scan_id: str):
    scan = await scans_collection.find_one({"_id": ObjectId(scan_id)})
    return scan

