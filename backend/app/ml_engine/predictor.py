# app/ml_engine/predictor.py
import os
from app.ml_engine.model import predict_text

def extract_text_from_file(file_path):
    # Simplified: only extract plain text from .txt/.log for now
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return " "

def analyze_file(file_path: str):
    raw_text = extract_text_from_file(file_path)
    label, confidence = predict_text(raw_text)
    
    return {
        "result": label,
        "threat_type": "heuristic" if label == "malicious" else None,
        "confidence": confidence,
        "message": "Scanned using hybrid ML model"
    }
