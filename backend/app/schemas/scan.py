# app/schemas/scan.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ScanResult(BaseModel):
    result: str
    threat_type: Optional[str]
    confidence: float
    message: str

class ScanRecordOut(BaseModel):
    filename: str
    result: str
    threat_type: Optional[str]
    confidence: float
    created_at: datetime
