from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"  # Заменим позже на реальное хеширование
    db_user = User(username=user.username, email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
