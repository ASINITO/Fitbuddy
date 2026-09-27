from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, WorkoutPlan, Feedback
from app.routes.auth import get_current_admin
from app.services.analytics_service import analytics_service

router = APIRouter(tags=["Admin & Analytics"])

@router.get("/api/admin/metrics")
def get_system_metrics(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Retrieve system analytics and metrics."""
    return analytics_service.get_admin_metrics(db)

@router.get("/api/admin/users")
def list_system_users(
    search: Optional[str] = None,
    goal: Optional[str] = None,
    level: Optional[str] = None,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Search and filter users across the platform without exposing password hashes."""
    query = db.query(User)
    
    if search:
        term = f"%{search}%"
        query = query.filter(
            (User.full_name.ilike(term)) |
            (User.username.ilike(term)) |
            (User.email.ilike(term))
        )
    if goal and goal != "All":
        query = query.filter(User.fitness_goal == goal)
    if level and level != "All":
        query = query.filter(User.fitness_level == level)

    users = query.order_by(User.created_at.desc()).all()
    
    return [
        {
            "id": u.id,
            "full_name": u.full_name,
            "username": u.username,
            "email": u.email,
            "is_admin": u.is_admin,
            "fitness_goal": u.fitness_goal,
            "fitness_level": u.fitness_level,
            "created_at": u.created_at.strftime("%Y-%m-%d"),
            "last_active": u.last_active.strftime("%Y-%m-%d %H:%M") if u.last_active else "N/A"
        }
        for u in users
    ]

@router.get("/api/admin/users/{user_id}")
def get_user_detail_admin(
    user_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Retrieve full user profile and workout stats for administrative review."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    plans_count = len(user.workout_plans)
    completed_workouts = len([wh for wh in user.workout_histories if wh.completed])

    return {
        "id": user.id,
        "full_name": user.full_name,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin,
        "age": user.age,
        "gender": user.gender,
        "height": user.height,
        "weight": user.weight,
        "fitness_level": user.fitness_level,
        "fitness_goal": user.fitness_goal,
        "preferred_intensity": user.preferred_intensity,
        "preferred_duration": user.preferred_duration,
        "available_days": user.available_days,
        "equipment": user.equipment,
        "dietary_preference": user.dietary_preference,
        "preferred_language": user.preferred_language,
        "created_at": user.created_at.strftime("%Y-%m-%d"),
        "total_plans_generated": plans_count,
        "completed_workouts": completed_workouts
    }

@router.get("/api/admin/feedbacks")
def get_all_feedbacks(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List all user feedback entries."""
    feedbacks = db.query(Feedback).order_by(Feedback.created_at.desc()).all()
    return [
        {
            "id": f.id,
            "user_id": f.user_id,
            "rating": f.rating,
            "category": f.category,
            "feedback_text": f.feedback_text,
            "created_at": f.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for f in feedbacks
    ]
