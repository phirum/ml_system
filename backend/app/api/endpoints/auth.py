# app/api/endpoints/auth.py
from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.auth import register_user, authenticate_user
from app.utils.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    new_user = await register_user(user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserOut(**new_user)

@router.post("/login")
async def login(user: UserLogin):
    auth_user = await authenticate_user(user)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(auth_user["_id"]), "role": auth_user["role"]})
    return {"access_token": token, "token_type": "bearer"}
