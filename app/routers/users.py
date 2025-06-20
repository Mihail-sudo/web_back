from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models
from app.database import get_db
from app.schemas import UserCreate, User, UserLogin
from app.crud import get_user_by_username, create_user, get_user_by_email, get_user_by_id
from app.core.auth import get_password_hash
from datetime import timedelta
from ..utils.access_token import create_access_token, get_current_user


router = APIRouter(prefix="/users", tags=["users"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="users/token")

@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user.password = get_password_hash(user.password)
    return create_user(db, user)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    if user.password + 'hashed_password' != db_user.hashed_password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(db_user.username, db_user.id, timedelta(hours=12))
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_me(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authorizing failed")
    db_user = get_user_by_id(db, id=user.get('id'))
    user_schema = {
        "username": db_user.username,
        "email": db_user.email,
        "created_at": db_user.created_at,
        "chats_count": len(db_user.chats),
        "total_messages": len(db_user.messages)
    }
    return {"user": user_schema}
