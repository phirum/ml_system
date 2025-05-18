from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import shutil
import os
from uuid import uuid4
from pydantic import BaseModel, HttpUrl
import re
from datetime import datetime

from app.services.scan import process_scan
from app.schemas.scan import ScanResult
from app.api.deps import get_current_user, require_admin
from app.db.scan import get_user_scans, get_all_scans, get_scan_by_id
from app.db.mongodb import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def _handle_file_scan(file: UploadFile, user_id: str) -> ScanResult:
    filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    scan_result = await process_scan(file_path, file.filename, user_id)
    return ScanResult(**scan_result)

# Generic file scan
@router.post("/file", response_model=ScanResult)
async def scan_file(file: UploadFile = File(...), user=Depends(get_current_user)):
    return await _handle_file_scan(file, user["id"])

# PDF scan
@router.post("/pdf", response_model=ScanResult)
async def scan_pdf(file: UploadFile = File(...), user=Depends(get_current_user)):
    return await _handle_file_scan(file, user["id"])

# Invoice/QR scan
@router.post("/invoice", response_model=ScanResult)
async def scan_invoice(file: UploadFile = File(...), user=Depends(get_current_user)):
    return await _handle_file_scan(file, user["id"])

# Network logs scan
@router.post("/network", response_model=ScanResult)
async def scan_network_logs(file: UploadFile = File(...), user=Depends(get_current_user)):
    return await _handle_file_scan(file, user["id"])

# User scan history
@router.get("/history")
async def get_user_history(user=Depends(get_current_user), db: AsyncIOMotorDatabase = Depends(get_database)):
    scans = await get_user_scans(user["id"], db)
    return {"count": len(scans), "scans": scans}

# All scans (admin only)
@router.get("/all")
async def get_all_scan_data(admin=Depends(require_admin), db: AsyncIOMotorDatabase = Depends(get_database)):
    scans = await get_all_scans(db)
    return {"count": len(scans), "scans": scans}

# Single scan by ID
@router.get("/{scan_id}")
async def get_single_scan(scan_id: str, user=Depends(get_current_user), db: AsyncIOMotorDatabase = Depends(get_database)):
    scan = await get_scan_by_id(scan_id, db)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan["user_id"] != user["id"] and user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return scan

# URL scan
class URLScanRequest(BaseModel):
    url: HttpUrl

@router.post("/url", response_model=ScanResult)
async def scan_url(request: URLScanRequest, user=Depends(get_current_user), db: AsyncIOMotorDatabase = Depends(get_database)):
    url = str(request.url)

    score = 0
    score += len(url) > 75
    score += url.count("-") > 1
    score += any(word in url.lower() for word in ["login", "verify", "update"])
    score += bool(re.search(r"\d+\.\d+\.\d+\.\d+", url))

    label = "MALICIOUS" if score >= 2 else "BENIGN"
    confidence = min(0.5 + score * 0.1, 0.99)

    scan_data = {
        "filename": url,
        "user_id": user["id"],
        "result": label,
        "threat_type": "phishing" if label == "MALICIOUS" else None,
        "confidence": confidence,
        "created_at": datetime.utcnow()
    }

    await db["scans"].insert_one(scan_data)

    return {
        "result": label,
        "threat_type": scan_data["threat_type"],
        "confidence": confidence,
        "message": f"URL Scan result: {label} with confidence {confidence:.2f}"
    }
