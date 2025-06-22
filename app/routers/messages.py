from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Message, Chat, User
from ..database import get_db
from ..utils.access_token import get_current_user
from ..schemas import SendMessage
import httpx
import json

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/send")
async def send_message(
    message: SendMessage,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    chat = db.query(Chat).filter(Chat.id == message.chat_id).first()
    if not chat or current_user["id"] not in [u.id for u in chat.participants]:
        raise HTTPException(status_code=403, detail="Нет доступа")

    new_message = Message(
        text=message.text,
        chat_id=message.chat_id,
        sender_id=current_user["id"]
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    if message.text.startswith('=='):
        try:
            async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
                response = await client.post("/ai/chat", json={"message": message.text}, timeout=30)
                text = json.loads(response.text)['response']

                new_message = Message(
                    text=text,
                    chat_id=message.chat_id,
                    sender_id=1
                )

                db.add(new_message)
                db.commit()
                db.refresh(new_message)

        except Exception as e:
            print(f"Ошибка: {type(e).__name__} — {e}")
            print('no no no mr fish')
            return {"message": 'Bot could not answer you'}

    # Уведомляем всех участников чата
    # notify_clients(message.chat_id, {
    #     "id": new_message.id,
    #     "content": new_message.text,
    #     "sender_id": new_message.sender_id,
    #     "timestamp": new_message.timestamp,
    # })

    return {"message": "Сообщение отправлено"}