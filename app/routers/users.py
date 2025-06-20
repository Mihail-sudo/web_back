from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, User, UserLogin
from app.crud import get_user_by_username, get_user_by_email, create_user
from app.core.auth import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

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
    return {'message': 'logged in'}
