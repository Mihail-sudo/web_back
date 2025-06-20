from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ChatCreate, Chat
from app.crud import create_chat
from..utils.access_token import get_current_user


router = APIRouter(prefix="/chats", tags=["chats"])

@router.post("/create", response_model=Chat)
def register_chat(chat: ChatCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authorizing failed")
    return create_chat(db, chat)
