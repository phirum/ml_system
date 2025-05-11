# app/api/endpoints/model.py
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
import shutil
import os
from app.api.deps import require_admin
from app.ml_engine.ml_trainer import train_from_csv
from app.db.retrain_log import log_retrain_event
from app.models.retrain_log import RetrainLog
from app.db.mongodb import get_database


router = APIRouter()

@router.post("/retrain", summary="Retrain ML Model from CSV", tags=["Model"])
async def retrain_model(
    file: UploadFile = File(...),
    admin_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed.")

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        result = train_from_csv(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")
    finally:
        os.remove(temp_path)

    # log to MongoDB
    retrain_log = RetrainLog(
        admin_id=admin_user["id"],
        admin_email=admin_user["email"],
        dataset_filename=file.filename,
        accuracy=result["metrics"]["accuracy"],
        f1_malicious=result["metrics"]["malicious_f1"],
        f1_benign=result["metrics"]["benign_f1"],
        model_version="v1.0"  # Optional: implement versioning later
    )
    await log_retrain_event(db, retrain_log)

    return {"message": "Model retrained", "metrics": result["metrics"]}
