# app/api/routes.py
from fastapi import APIRouter

from app.api.endpoints import auth, scan

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(scan.router, prefix="/scan", tags=["Scan"])
