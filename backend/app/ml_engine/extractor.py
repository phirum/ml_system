# app/ml_engine/extractor.py
def extract_features_from_text(text: str) -> dict:
    return {
        "Feature1": len(text),
        "Feature2": sum(c.isdigit() for c in text),
        "Feature3": sum(c.isupper() for c in text),
        "Feature4": int("http" in text),
        "Feature5": len(text.split())
    }
