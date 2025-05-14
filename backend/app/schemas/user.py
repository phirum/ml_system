# app/schemas/user.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "user"  # or 'admin', 'analyst', etc.
    username: str

class UserLogin(BaseModel):
    identifier: str  # can be email or username
    password: str

class UserOut(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: str
