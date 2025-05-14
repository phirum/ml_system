# app/api/api_v1/api.py
from app.api.endpoints import model
from app.api.endpoints import auth, scan, user


api_router.include_router(model.router, prefix="/model")
api_router.include_router(user.router, prefix="/users")
api_router.include_router(scan.router, prefix="/scan")
api_router.include_router(auth.router, prefix="/auth")

