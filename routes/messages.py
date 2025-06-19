from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import MessageCreate, Message
from crud import send_message, get_messages

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=Message)
def send(msg: MessageCreate, db: Session = Depends(get_db), user_id: int = 1):  # временно
    return send_message(db, msg, user_id)

@router.get("/{contact_id}", response_model=list[Message])
def get(contact_id: int, db: Session = Depends(get_db), user_id: int = 1):  # временно
    return get_messages(db, user_id, contact_id)