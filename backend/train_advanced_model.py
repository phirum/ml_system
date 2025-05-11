# train_advanced_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

# Load dataset
df = pd.read_csv("data/malware_data.csv")

# Basic cleaning
df = df.dropna(subset=["text", "label"])
df = df[df["label"].isin(["malicious", "benign"])]  # Only 2 classes

# Split
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

# TF-IDF vectorization
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train ML model
model = RandomForestClassifier(n_estimators=100, max_depth=30, random_state=42)
model.fit(X_train_tfidf, y_train)

# Evaluation
y_pred = model.predict(X_test_tfidf)
print(classification_report(y_test, y_pred))

# Save model and vectorizer
os.makedirs("app/ml_engine", exist_ok=True)
joblib.dump(model, "app/ml_engine/model.joblib")
joblib.dump(vectorizer, "app/ml_engine/vectorizer.joblib")

print("✅ Trained model and vectorizer saved successfully.")
