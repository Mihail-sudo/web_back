from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, chats
from .models import *

app = FastAPI()

app.include_router(users.router)
app.include_router(chats.router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Messenger API is running"}


