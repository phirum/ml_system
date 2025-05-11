# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables if present

class Settings:
    PROJECT_NAME: str = "Malware Analysis"
    DB_URI: str = os.getenv("DB_URI", "mongodb://localhost:27017")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecret")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()
