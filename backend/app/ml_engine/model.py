# app/ml_engine/model.py
import os
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

MODEL_PATH = "app/ml_engine/model.joblib"
VECTORIZER_PATH = "app/ml_engine/vectorizer.joblib"

# Load model & vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def predict_text(text: str):
    features = vectorizer.transform([text])
    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0]
    confidence = round(np.max(proba), 2)
    return prediction, confidence
