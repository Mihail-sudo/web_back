from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Chat, User
from ..utils.access_token import get_current_user

router = APIRouter(tags=["WebSocket"])

active_connections = {}

@router.websocket("/ws/{chat_id}")
async def websocket_chat(
    websocket: WebSocket,
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    await websocket.accept()

    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat or db.query(User).get(current_user["id"]) not in chat.participants:
        await websocket.close(code=403)
        return

    if chat_id not in active_connections:
        active_connections[chat_id] = []

    active_connections[chat_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections[chat_id].remove(websocket)

async def notify_clients(chat_id: int, message_data: dict):
    if chat_id in active_connections:
        for connection in active_connections[chat_id]:
            await connection.send_json(message_data)