from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, ChatMessage
from app.schemas import ChatMessageCreate
from app.routes.auth import get_current_user
from app.services.gemini_service import gemini_service

router = APIRouter(tags=["AI Fitness Chatbot"])

@router.post("/api/chat")
def chat_with_fitbuddy(
    chat_in: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Interact with FitBuddy AI fitness coach in English or Tamil."""
    user_lang = chat_in.language or current_user.preferred_language or "English"

    # Save user message
    user_msg = ChatMessage(
        user_id=current_user.id,
        sender="user",
        message=chat_in.message,
        language=user_lang
    )
    db.add(user_msg)
    db.commit()

    # Fetch last 6 messages for context
    recent_msgs = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).order_by(ChatMessage.created_at.desc()).limit(6).all()
    
    history_payload = [
        {"sender": m.sender, "message": m.message}
        for m in reversed(recent_msgs)
    ]

    profile = {
        "full_name": current_user.full_name,
        "fitness_goal": current_user.fitness_goal,
        "fitness_level": current_user.fitness_level,
        "equipment": current_user.equipment,
        "dietary_preference": current_user.dietary_preference
    }

    ai_reply = gemini_service.fitness_chat(
        message=chat_in.message,
        profile=profile,
        history=history_payload,
        language=user_lang
    )

    # Save AI response
    ai_msg = ChatMessage(
        user_id=current_user.id,
        sender="ai",
        message=ai_reply,
        language=user_lang
    )
    db.add(ai_msg)
    db.commit()

    return {
        "reply": ai_reply,
        "language": user_lang,
        "user_message_id": user_msg.id,
        "ai_message_id": ai_msg.id
    }

@router.get("/api/chat/history")
def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get previous chat messages for current user."""
    msgs = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).order_by(ChatMessage.created_at.asc()).limit(50).all()

    return [
        {
            "id": m.id,
            "sender": m.sender,
            "message": m.message,
            "language": m.language,
            "timestamp": m.created_at.strftime("%I:%M %p")
        }
        for m in msgs
    ]
