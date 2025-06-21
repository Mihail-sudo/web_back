from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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
    chat_id: int,
    user_names: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Получаем чат
    db_chat = db.query(Chat).get(chat_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Чат не найден")

    # Проверяем, что текущий пользователь — участник чата
    if current_user["id"] != db_chat.owner_id:
        raise HTTPException(status_code=403, detail="Вы не админ этого чата")

    # Получаем пользователя, которого хотим добавить
    new_faces = []
    for user_name in user_names:
        new_user = db.query(models.User).filter(models.User.username == user_name).first()
        if new_user:
            if new_user not in db_chat.participants:
                new_faces.append(new_user.username)
                db_chat.participants.append(new_user)
    db.commit()
    new_faces = ', '.join(new_faces)
    return {"message": f"Пользователи {new_faces} добавлен в чат"}

