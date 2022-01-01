from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# TODO: Figure out better way to get optional args
class UserOut(BaseModel):
    id: Optional[int]
    email: Optional[EmailStr]
    createdAt: Optional[datetime]

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    msg: str
