from pydantic import BaseModel, EmailStr
from typing import Literal, Optional


class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Literal["admin", "user"]
    status: Optional[str] = "active"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[Literal["admin", "user"]] = None
    status: Optional[str] = None



class UserOut(UserBase):
    id: str


class UserInDB(UserBase):
    id: Optional[str]
    hashed_password: str
