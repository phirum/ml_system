# app/services/auth.py
from app.utils.security import hash_password, verify_password, create_access_token
from app.models.user import UserInDB
from app.schemas.user import UserCreate, UserLogin
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.DB_URI)
db = client["malware_analysis"]
users_collection = db["users"]

async def register_user(user: UserCreate):
    existing = await users_collection.find_one({
        "$or": [{"email": user.email}, {"username": user.username}]
    })
    if existing:
        return None

    user_dict = {
        "email": user.email,
        "username": user.username,
        "hashed_password": hash_password(user.password),
        "full_name": user.full_name,
        "role": "user"
    }
    await users_collection.insert_one(user_dict)
    return user_dict

async def authenticate_user(user: UserLogin):
    db_user = await users_collection.find_one({
        "$or": [{"email": user.identifier}, {"username": user.identifier}]
    })
    if not db_user:
        return None
    if not verify_password(user.password, db_user["hashed_password"]):
        return None
    return db_user

