# app/ml_engine/ml_trainer.py
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def train_from_csv(file_path: str) -> dict:
    df = pd.read_csv(file_path)
    print("Loaded dataset:", df.shape)

    if "Label" not in df.columns:
        raise ValueError("Dataset must contain a 'Label' column.")

    # Optional: Drop rows with missing or null labels
    df = df.dropna(subset=["Label"])

    # Features and target
    X = df.drop(columns=["Label"])
    y = df["Label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)

    model_path = os.path.join(os.path.dirname(__file__), "model.joblib")
    joblib.dump({
        "model": model,
        "feature_names": list(X.columns),
        "classes": model.classes_.tolist()  # Save the label classes
    }, model_path)

    metrics = {
        "accuracy": report["accuracy"],
        "macro_f1": report["macro avg"]["f1-score"],
        "weighted_f1": report["weighted avg"]["f1-score"]
    }

    return {"metrics": metrics}
