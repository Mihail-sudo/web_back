from pydantic import BaseModel
from datetime import datetime
from typing_extensions import Optional, List


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


class ChatCreate(BaseModel):
    name: str


class ChatBase(BaseModel):
    name: str = None
    owner_id: int


class Chat(ChatBase):
    id: int
    created_at: datetime
    participants: List[User] = []

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    type_token: str


class SendMessage(BaseModel):
    chat_id: int
    text: str
