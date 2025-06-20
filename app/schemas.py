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


class ChatBase(BaseModel):
    name: Optional[str] = None
    is_ai_chat: bool = False


class ChatCreate(ChatBase):
    created_at: datetime
    participants: List[User] = []


class Chat(ChatBase):
    id: int
    created_at: datetime
    participants: List[User] = []

    class Config:
        from_attributes = True