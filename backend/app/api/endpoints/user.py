from fastapi import APIRouter, HTTPException, Depends
from app.api.deps import get_database, require_admin
from app.db import user as user_crud
from app.models import user as user_model
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.post("/", tags=["User"])
async def create_user(user: user_model.UserCreate, db: AsyncIOMotorDatabase = Depends(get_database),
                      admin=Depends(require_admin)):
    existing = await user_crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    uid = await user_crud.create_user(db, user.dict())
    return {"message": "User created", "user_id": uid}

@router.get("/", tags=["User"])
async def list_users(db: AsyncIOMotorDatabase = Depends(get_database),
                     admin=Depends(require_admin)):
    users = await user_crud.list_users(db)
    return users

@router.put("/{user_id}", tags=["User"])
async def update_user(user_id: str, updates: user_model.UserUpdate,
                      db: AsyncIOMotorDatabase = Depends(get_database),
                      admin=Depends(require_admin)):
    await user_crud.update_user(db, user_id, updates.dict(exclude_unset=True))
    return {"message": "User updated"}

@router.delete("/{user_id}", tags=["User"])
async def delete_user(user_id: str,
                      db: AsyncIOMotorDatabase = Depends(get_database),
                      admin=Depends(require_admin)):
    await user_crud.delete_user(db, user_id)
    return {"message": "User deleted"}
