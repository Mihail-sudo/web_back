from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Message, Chat, User
from ..database import get_db
from ..utils.access_token import get_current_user
from ..schemas import SendMessage

router = APIRouter(prefix="/messages", tags=["messages"])

# Импортируем active_connections и notify_clients
from .chat_ws import active_connections, notify_clients

@router.post("/send")
def send_message(
    message: SendMessage,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Проверяем существование чата и доступ
    chat = db.query(Chat).filter(Chat.id == message.chat_id).first()
    if not chat or current_user["id"] not in [u.id for u in chat.participants]:
        raise HTTPException(status_code=403, detail="Нет доступа")

    # Создаём сообщение
    new_message = Message(
        text=message.text,
        chat_id=message.chat_id,
        sender_id=current_user["id"]
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    # Уведомляем всех участников чата
    notify_clients(message.chat_id, {
        "id": new_message.id,
        "content": new_message.text,
        "sender_id": new_message.sender_id,
        "timestamp": new_message.timestamp,
    })

    return {"message": "Сообщение отправлено"}