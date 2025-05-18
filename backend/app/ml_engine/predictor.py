# app/ml_engine/predictor.py
import os
from app.ml_engine.model import predict_text

def analyze_file(file_path: str):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_text = f.read()

    label, confidence = predict_text(raw_text)

    return {
        "filename": os.path.basename(file_path),
        "label": label,
        "confidence": confidence,
        "message": f"Prediction complete: {label} with confidence {confidence:.2f}"
    }
