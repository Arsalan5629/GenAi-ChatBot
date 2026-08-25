from sqlalchemy.sql import func

from database import SessionLocal
from models import ChatSession, Message


def create_chat(title="New Chat"):
    db = SessionLocal()

    try:
        chat = ChatSession(title=title)

        db.add(chat)
        db.commit()
        db.refresh(chat)

        return chat.id

    finally:
        db.close()


def get_all_chats():
    db = SessionLocal()

    try:
        return (
            db.query(ChatSession)
            .order_by(ChatSession.updated_at.desc())
            .all()
        )

    finally:
        db.close()


def save_message(chat_id, role, content):
    db = SessionLocal()

    try:
        message = Message(
            session_id=chat_id,
            role=role,
            content=content
        )

        db.add(message)

        chat = (
            db.query(ChatSession)
            .filter(ChatSession.id == chat_id)
            .first()
        )

        if chat:
            chat.updated_at = func.now()

        db.commit()
        db.refresh(message)

        return message

    finally:
        db.close()


def get_messages(chat_id):
    db = SessionLocal()

    try:
        return (
            db.query(Message)
            .filter(Message.session_id == chat_id)
            .order_by(Message.created_at.asc())
            .all()
        )

    finally:
        db.close()


def update_chat_title(chat_id, title):
    db = SessionLocal()

    try:
        chat = (
            db.query(ChatSession)
            .filter(ChatSession.id == chat_id)
            .first()
        )

        if chat:
            chat.title = title
            db.commit()

    finally:
        db.close()


def delete_chat(chat_id):
    db = SessionLocal()

    try:
        chat = (
            db.query(ChatSession)
            .filter(ChatSession.id == chat_id)
            .first()
        )

        if chat:
            db.delete(chat)
            db.commit()

    finally:
        db.close()