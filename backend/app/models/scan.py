from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from bson import ObjectId


class ScanRecord(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    id: Optional[ObjectId] = Field(alias="_id")
    filename: str
    user_id: str
    result: str
    threat_type: Optional[str]
    confidence: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
