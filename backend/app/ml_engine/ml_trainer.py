# app/ml_engine/ml_trainer.py
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def train_from_csv(file_path: str) -> dict:
    try:
        df = pd.read_csv(file_path)
        print("Loaded dataset from csv to train:", df.shape)

        if "Label" not in df.columns:
            raise ValueError("Dataset must contain a 'Label' column.")

        df = df[df["Label"].isin(["BENIGN", "MALICIOUS"])]

        X = df.drop(columns=["Label"])
        y = df["Label"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )

        model = RandomForestClassifier(n_estimators=100, max_depth=30)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)

        joblib.dump(model, "app/ml_engine/model.joblib")

        return {
            "status": "success",
            "metrics": {
                "accuracy": round(report["accuracy"], 3),
                "malicious_f1": round(report.get("MALICIOUS", {}).get("f1-score", 0.0), 3),
                "benign_f1": round(report.get("BENIGN", {}).get("f1-score", 0.0), 3)
            }
        }

    except Exception as e:
        print("\n❌ Error during model training:", str(e))
        raise RuntimeError(f"Training failed: {str(e)}")
