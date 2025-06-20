from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, User
from app.crud import get_user_by_username, create_user
from app.core.auth import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    user.password = get_password_hash(user.password)
    return create_user(db, user)
