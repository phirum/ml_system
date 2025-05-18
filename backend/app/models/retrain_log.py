# app/models/retrain_log.py
from pydantic import BaseModel, Field
from datetime import datetime

class RetrainLog(BaseModel):
    admin_id: str
    admin_email: str
    dataset_filename: str
    accuracy: float
    f1_malicious: float
    f1_benign: float
    model_version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        protected_namespaces = ()



