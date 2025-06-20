# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chats = relationship("Chat", secondary="chat_participants", back_populates="participants")
    messages = relationship("Message", back_populates="sender")


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    is_ai_chat = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    participants = relationship("User", secondary="chat_participants", back_populates="chats")
    messages = relationship("Message", back_populates="chat")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String)
    is_ai_message = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="messages")


class ChatParticipant(Base):
    __tablename__ = "chat_participants"
    chat_id = Column(Integer, ForeignKey("chats.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
