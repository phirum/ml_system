# app/api/endpoints/model.py
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
import shutil
import os
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.deps import require_admin
from app.ml_engine.ml_trainer import train_from_csv
from app.db.retrain_log import log_retrain_event, get_all_retrain_logs
from app.models.retrain_log import RetrainLog
from app.db.mongodb import get_database

router = APIRouter()

@router.post("/retrain", summary="Retrain ML Model from CSV", tags=["Model"])
async def retrain_model(
    file: UploadFile = File(...),
    admin_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    try:
        print("Received file for retraining:", file.filename)
        
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files allowed.")

        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        result = train_from_csv(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")
    finally:
        os.remove(temp_path)

    metrics = result["metrics"]
    f1_scores = metrics.get("f1_scores", {})

    retrain_log = RetrainLog(
        admin_id=admin_user["id"],
        admin_email=admin_user["email"],
        dataset_filename=file.filename,
        accuracy=metrics.get("accuracy", 0.0),
        f1_malicious=f1_scores.get("MALICIOUS", 0.0),
        f1_benign=f1_scores.get("BENIGN", 0.0),
        model_version="v1.0"
    )
    await log_retrain_event(db, retrain_log)

    return {
        "message": "Model retrained successfully",
        "metrics": metrics
    }


# ✅ NEW: Fetch all retrain logs
@router.get("/retrain/logs", summary="Get model retraining logs", tags=["Model"])
async def get_retrain_logs(
    admin_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    logs = await get_all_retrain_logs(db)
    return logs
