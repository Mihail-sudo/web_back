from sqlalchemy.orm import Session
from . import models, schemas

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def send_message(db: Session, message: schemas.MessageCreate, user_id: int):
    db_message = models.Message(
        sender_id=user_id,
        receiver_id=message.receiver_id,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, user_id: int, contact_id: int):
    return db.query(models.Message).filter(
        ((models.Message.sender_id == user_id) & (models.Message.receiver_id == contact_id)) |
        ((models.Message.sender_id == contact_id) & (models.Message.receiver_id == user_id))
    ).all()