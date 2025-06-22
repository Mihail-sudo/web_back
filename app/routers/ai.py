from fastapi import APIRouter, Depends
from langchain_ollama import ChatOllama

router = APIRouter(prefix="/ai", tags=["AI"])

llm = ChatOllama(model="llama3.2:3b",
                 base_url='http://localhost:11434/')

@router.post("/chat")
async def chat_with_ai(message: dict):
    msg = message.get("message")
    response = await llm.ainvoke(msg)
    return {"response": response.content}
