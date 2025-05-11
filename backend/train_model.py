# train_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

# Sample dataset (you can replace this with real malware data)
data = {
    "text": [
        "This is a ransomware attack script",
        "def encrypt_files(): pass",
        " harmless pdf file document ",
        "user login failed multiple times",
        "malicious code found in binary",
        "legitimate business invoice",
        "network connection from unknown host",
        "safe file with no issue",
    ],
    "label": [
        "malicious", "malicious", "benign", "malicious",
        "malicious", "benign", "malicious", "benign"
    ]
}

df = pd.DataFrame(data)

# Text vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])
y = df["label"]

# Split for training/testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model and vectorizer
joblib.dump(model, "app/ml_engine/model.joblib")
joblib.dump(vectorizer, "app/ml_engine/vectorizer.joblib")

print("✅ Model and vectorizer saved successfully.")
