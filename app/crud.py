from sqlalchemy.orm import Session
from app.models import User, Chat
from app.schemas import UserCreate, ChatCreate
from datetime import datetime

def get_user_by_id(db: Session, id: int):
    return db.query(User).get(id)

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_chat(db: Session, chat: ChatCreate):
    db_chat = Chat(name=chat.name, is_ai_chat=chat.is_ai_chat, created_at=datetime.now(), participants=chat.participants)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat
