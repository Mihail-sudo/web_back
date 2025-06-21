from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.schemas import Chat, ChatCreate
from app.crud import create_chat
from ..utils.access_token import get_current_user
from ..crud import get_user_by_id
from .. import models


router = APIRouter(prefix="/chats", tags=["chats"])

@router.post("/create", response_model=Chat)
def register_chat(chat: ChatCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authorizing failed")
    return create_chat(db, chat, id=user.get('id'))

@router.get("/")
def chats_main(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authorizing failed")    
    db_user = get_user_by_id(db, id=user.get('id'))

    return {
        "user": db_user.username,
        "chats": db_user.chats
    }

@router.post("/{chat_id}/add-users")
def add_user_to_chat(
    data: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    chat_id = data.get('chat_id')
    user_names = data.get('user_names')
    # Получаем чат
    db_chat = db.query(models.Chat).get(chat_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Чат не найден")

    # Проверяем, что текущий пользователь — участник чата
    if current_user["id"] != db_chat.owner_id:
        raise HTTPException(status_code=403, detail="Вы не админ этого чата")

    # Получаем пользователя, которого хотим добавить
    user_names = user_names.split(';')
    new_faces = []
    for user_name in user_names:
        new_user = db.query(models.User).filter(models.User.username == user_name).first()
        if new_user:
            if new_user not in db_chat.participants:
                new_faces.append(new_user.username)
                db_chat.participants.append(new_user)
    db.add(db_chat)
    db.commit()
    new_faces = ', '.join(new_faces)
    return {"message": f"Пользователи {new_faces} добавлен в чат"}

@router.get("/{chat_id}/messages")
def get_chat_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Ищем чат с участниками и сообщениями
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")
    if current_user["id"] not in [u.id for u in chat.participants]:
        raise HTTPException(status_code=403, detail="Нет доступа")

    # Получаем сообщения
    messages = db.query(models.Message).options(joinedload(models.Message.sender)).filter(models.Message.chat_id == chat_id).all()
    
    result = [
        {
            "id": msg.id,
            "text": msg.text,
            "chat_id": msg.chat_id,
            "sender_id": msg.sender_id,
            "sender_name": msg.sender.username,  # <-- получаем имя пользователя
            "timestamp": msg.timestamp
        }
        for msg in messages
    ]

    return result
