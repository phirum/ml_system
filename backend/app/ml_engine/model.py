# app/ml_engine/model.py
import joblib
import pandas as pd
import os
from app.ml_engine.extractor import extract_features_from_text

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")

model = None
expected_features = None

def load_model():
    global model, expected_features
    if model is None or expected_features is None:
        model_data = joblib.load(MODEL_PATH)
        model = model_data["model"]
        expected_features = model_data["feature_names"]

def predict_text(raw_text: str):
    load_model()
    features = extract_features_from_text(raw_text)
    df = pd.DataFrame([features])[expected_features]
    label = model.predict(df)[0]
    confidence = max(model.predict_proba(df)[0])
    return label, confidence
