from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ChatCreate, Chat
from app.crud import create_chat


router = APIRouter(prefix="/chats", tags=["chats"])

@router.post("/create", response_model=Chat)
def register_chat(chat: ChatCreate, db: Session = Depends(get_db)):    
    return create_chat(db, chat)
