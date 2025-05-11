# app/ml_engine/ml_trainer.py
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def train_from_csv(file_path: str) -> dict:
    df = pd.read_csv(file_path)
    df = df.dropna(subset=["text", "label"])
    df = df[df["label"].isin(["malicious", "benign"])]

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.2, stratify=df["label"], random_state=42
    )

    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, max_depth=30)
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)
    report = classification_report(y_test, y_pred, output_dict=True)

    # Save updated model and vectorizer
    joblib.dump(model, "app/ml_engine/model.joblib")
    joblib.dump(vectorizer, "app/ml_engine/vectorizer.joblib")

    return {
        "status": "success",
        "metrics": {
            "accuracy": round(report["accuracy"], 3),
            "malicious_f1": round(report["malicious"]["f1-score"], 3),
            "benign_f1": round(report["benign"]["f1-score"], 3)
        }
    }
