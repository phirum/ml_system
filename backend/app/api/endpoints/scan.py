# app/api/endpoints/scan.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import shutil
import os
from uuid import uuid4
from app.services.scan import process_scan
from app.schemas.scan import ScanResult

router = APIRouter()

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/file", response_model=ScanResult)
async def scan_file(file: UploadFile = File(...)):
    # TEMP: Assume user_id is fixed (replace with auth later)
    user_id = "1234567890"
    
    filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    scan_result = await process_scan(file_path, file.filename, user_id)
    return ScanResult(**scan_result)

# app/api/endpoints/scan.py (continued)
from app.api.deps import get_current_user, require_admin

@router.get("/history")
async def get_user_history(user=Depends(get_current_user)):
    scans = await get_user_scans(user["id"])
    return {"count": len(scans), "scans": scans}

@router.get("/all")
async def get_all_scan_data(admin=Depends(require_admin)):
    scans = await get_all_scans()
    return {"count": len(scans), "scans": scans}

@router.get("/{scan_id}")
async def get_single_scan(scan_id: str, user=Depends(get_current_user)):
    scan = await get_scan_by_id(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    # only allow users to see their own scans or admins
    if scan["user_id"] != user["id"] and user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return scan
