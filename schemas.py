from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class MessageCreate(BaseModel):
    receiver_id: int
    content: str

class Message(MessageCreate):
    id: int
    sender_id: int
    timestamp: str

    class Config:
        orm_mode = True
    