from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
import shutil
import os
from typing import List

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

    retrain_log = RetrainLog(
        admin_id=admin_user["id"],
        admin_email=admin_user["email"],
        dataset_filename=file.filename,
        accuracy=result["metrics"]["accuracy"],
        f1_malicious=result["metrics"]["malicious_f1"],
        f1_benign=result["metrics"]["benign_f1"],
        model_version="v1.0"
    )
    await log_retrain_event(db, retrain_log)

    return {"message": "Model retrained", "metrics": result["metrics"]}


@router.get("/retrain/logs", response_model=List[RetrainLog], summary="Get retraining log history", tags=["Model"])
async def fetch_retrain_logs(
    db: AsyncIOMotorDatabase = Depends(get_database),
    admin_user: dict = Depends(require_admin)
):
    logs = await get_all_retrain_logs(db)
    return logs
