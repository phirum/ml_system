# /app/db/user.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from passlib.hash import bcrypt


async def create_user(db: AsyncIOMotorDatabase, user_data: dict):
    user_data["hashed_password"] = bcrypt.hash(user_data.pop("password"))
    result = await db.users.insert_one(user_data)
    return str(result.inserted_id)


async def get_user_by_email(db, email: str):
    return await db.users.find_one({"email": email})


async def list_users(db):
    cursor = db.users.find({})
    users = []
    async for u in cursor:
        u["id"] = str(u["_id"])
        u.pop("_id", None)
        u.pop("hashed_password", None)
        users.append(u)
    return users


async def update_user(db, user_id: str, update_data: dict):
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})


async def delete_user(db, user_id: str):
    await db.users.delete_one({"_id": ObjectId(user_id)})
