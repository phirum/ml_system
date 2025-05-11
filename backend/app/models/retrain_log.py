# app/models/retrain_log.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class RetrainLog(BaseModel):
    admin_id: str
    admin_email: str
    dataset_filename: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    accuracy: float
    f1_malicious: float
    f1_benign: float
    model_version: Optional[str] = None
