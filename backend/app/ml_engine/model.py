# app/ml_engine/model.py
import joblib
import pandas as pd
import os
from app.ml_engine.extractor import extract_features_from_text

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")

model = None
expected_features = None

# Load model once
model_data = joblib.load(MODEL_PATH)
model = model_data["model"]
feature_names = model_data["feature_names"]
class_labels = model_data.get("classes", model.classes_.tolist())  # Fallback if 'classes' not stored


def load_model():
    global model, expected_features
    if model is None or expected_features is None:
        model_data = joblib.load(MODEL_PATH)
        model = model_data["model"]
        expected_features = model_data["feature_names"]

#
def predict_text(text: str) -> tuple[str, float]:
    features = extract_features_from_text(text)

    # Create feature vector in expected order
    vector = np.array([[features.get(name, 0) for name in feature_names]])

    # Predict class label and get probability
    predicted_index = model.predict(vector)[0]
    probabilities = model.predict_proba(vector)[0]
    confidence = float(np.max(probabilities))

    predicted_label = predicted_index if isinstance(predicted_index, str) else class_labels[int(predicted_index)]

    return predicted_label, confidence
