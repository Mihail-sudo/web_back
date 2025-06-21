from sqlalchemy.orm import Session
from app.models import User, Chat
from app.schemas import UserCreate
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

def create_chat(db: Session, chat: Chat, id):
    user = get_user_by_id(db, id)
    db_chat = Chat(name=chat.name, created_at=datetime.now(), participants=[], owner_id=id)
    db_chat.participants.append(user)
    
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat
