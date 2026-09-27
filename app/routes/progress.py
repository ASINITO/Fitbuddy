import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import (
    User, Progress, WaterLog, SleepLog, DailyCheckIn,
    Achievement, UserAchievement, Feedback
)
from app.schemas import (
    ProgressCreate, WaterLogCreate, SleepLogCreate,
    DailyCheckInCreate, FeedbackCreate
)
from app.routes.auth import get_current_user
from app.services.recommendation_service import recommendation_service
from app.utils.helpers import check_and_award_achievements, calculate_user_streak

router = APIRouter(tags=["Tracking & Progress"])

# --- Hydration ---
@router.post("/api/water")
def log_water_intake(
    water_in: WaterLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log water intake for today."""
    today_start = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    water_log = db.query(WaterLog).filter(
        WaterLog.user_id == current_user.id,
        WaterLog.date >= today_start
    ).first()

    if not water_log:
        water_log = WaterLog(
            user_id=current_user.id,
            glasses=water_in.glasses,
            amount_ml=water_in.amount_ml,
            daily_target_ml=water_in.daily_target_ml or 2500
        )
        db.add(water_log)
    else:
        water_log.glasses = water_in.glasses
        water_log.amount_ml = water_in.amount_ml
        if water_in.daily_target_ml:
            water_log.daily_target_ml = water_in.daily_target_ml

    db.commit()
    db.refresh(water_log)
    
    new_badges = check_and_award_achievements(db, current_user)
    
    percentage = min(100, round((water_log.amount_ml / max(1, water_log.daily_target_ml)) * 100))
    return {
        "glasses": water_log.glasses,
        "amount_ml": water_log.amount_ml,
        "daily_target_ml": water_log.daily_target_ml,
        "percentage": percentage,
        "new_achievements": new_badges
    }

@router.get("/api/water")
def get_water_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get past 7 days of water intake logs."""
    logs = db.query(WaterLog).filter(
        WaterLog.user_id == current_user.id
    ).order_by(WaterLog.date.desc()).limit(7).all()
    
    return [
        {
            "id": l.id,
            "date": l.date.strftime("%Y-%m-%d"),
            "amount_ml": l.amount_ml,
            "glasses": l.glasses,
            "target_ml": l.daily_target_ml,
            "percentage": min(100, round((l.amount_ml / max(1, l.daily_target_ml)) * 100))
        }
        for l in reversed(logs)
    ]

# --- Sleep ---
@router.post("/api/sleep")
def log_sleep(
    sleep_in: SleepLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record sleep metrics and get recovery suggestions."""
    sleep_log = SleepLog(
        user_id=current_user.id,
        sleep_time=sleep_in.sleep_time,
        wake_time=sleep_in.wake_time,
        duration_hours=sleep_in.duration_hours,
        sleep_quality=sleep_in.sleep_quality,
        recovery_note=sleep_in.recovery_note
    )
    db.add(sleep_log)
    db.commit()
    db.refresh(sleep_log)
    
    return {
        "id": sleep_log.id,
        "duration_hours": sleep_log.duration_hours,
        "quality": sleep_log.sleep_quality,
        "date": sleep_log.date.strftime("%Y-%m-%d")
    }

@router.get("/api/sleep")
def get_sleep_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get past 7 days of sleep records."""
    logs = db.query(SleepLog).filter(
        SleepLog.user_id == current_user.id
    ).order_by(SleepLog.date.desc()).limit(7).all()
    
    return [
        {
            "id": l.id,
            "date": l.date.strftime("%Y-%m-%d"),
            "duration": l.duration_hours,
            "quality": l.sleep_quality,
            "sleep_time": l.sleep_time,
            "wake_time": l.wake_time
        }
        for l in reversed(logs)
    ]

# --- Daily Check-in ---
@router.post("/api/checkin")
def submit_daily_checkin(
    checkin_in: DailyCheckInCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit daily wellness check-in and receive immediate AI recommendation."""
    checkin = DailyCheckIn(
        user_id=current_user.id,
        energy_level=checkin_in.energy_level,
        mood=checkin_in.mood,
        sleep_quality=checkin_in.sleep_quality,
        muscle_soreness=checkin_in.muscle_soreness,
        stress_level=checkin_in.stress_level,
        workout_completed=checkin_in.workout_completed,
        water_intake_ml=checkin_in.water_intake_ml
    )
    db.add(checkin)
    db.commit()
    db.refresh(checkin)

    ai_rec = recommendation_service.generate_recommendation_for_user(db, current_user)
    checkin.ai_recommendation = ai_rec
    db.commit()

    new_badges = check_and_award_achievements(db, current_user)
    current_streak, longest_streak = calculate_user_streak(db, current_user.id)

    return {
        "success": True,
        "recommendation": ai_rec,
        "streak": current_streak,
        "longest_streak": longest_streak,
        "new_achievements": new_badges
    }

# --- General Progress ---
@router.post("/api/progress")
def log_progress(
    progress_in: ProgressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log body measurements, running distance, or strength achievements."""
    entry = Progress(
        user_id=current_user.id,
        weight=progress_in.weight,
        chest=progress_in.chest,
        waist=progress_in.waist,
        arms=progress_in.arms,
        steps=progress_in.steps,
        running_distance=progress_in.running_distance,
        strength_record=progress_in.strength_record,
        notes=progress_in.notes
    )
    db.add(entry)
    
    if progress_in.weight:
        current_user.weight = progress_in.weight
        
    db.commit()
    db.refresh(entry)
    return {"message": "Progress logged successfully.", "id": entry.id}

@router.get("/api/progress")
def get_progress_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all historical progress records."""
    logs = db.query(Progress).filter(
        Progress.user_id == current_user.id
    ).order_by(Progress.date.asc()).limit(30).all()
    
    return [
        {
            "id": l.id,
            "date": l.date.strftime("%Y-%m-%d"),
            "weight": l.weight,
            "steps": l.steps,
            "running_distance": l.running_distance,
            "waist": l.waist,
            "strength": l.strength_record
        }
        for l in logs
    ]

# --- Streaks & Badges ---
@router.get("/api/streaks")
def get_streak_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve current workout streak and weekly completion rate."""
    current_streak, longest_streak = calculate_user_streak(db, current_user.id)
    
    # Calculate weekly completion percentage
    week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    completed_this_week = db.query(WorkoutHistory).filter(
        WorkoutHistory.user_id == current_user.id,
        WorkoutHistory.completed == True,
        WorkoutHistory.completed_at >= week_ago
    ).count()
    target_days = current_user.available_days or 4
    weekly_rate = min(100, round((completed_this_week / max(1, target_days)) * 100))

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "weekly_completion_rate": weekly_rate,
        "workouts_this_week": completed_this_week,
        "target_weekly_workouts": target_days
    }

@router.get("/api/achievements")
def get_user_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all badges with unlocked statuses for current user."""
    all_badges = db.query(Achievement).all()
    unlocked = {
        ua.achievement_id: ua.unlocked_at
        for ua in db.query(UserAchievement).filter(UserAchievement.user_id == current_user.id).all()
    }

    return [
        {
            "id": b.id,
            "code": b.code,
            "title": b.title,
            "description": b.description,
            "icon": b.icon,
            "category": b.category,
            "points": b.points,
            "unlocked": b.id in unlocked,
            "unlocked_at": unlocked[b.id].strftime("%b %d, %Y") if b.id in unlocked else None
        }
        for b in all_badges
    ]

# --- Feedback ---
@router.post("/api/feedback")
def submit_feedback(
    feedback_in: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit platform feedback with 1-5 rating."""
    fb = Feedback(
        user_id=current_user.id,
        rating=feedback_in.rating,
        category=feedback_in.category,
        feedback_text=feedback_in.feedback_text
    )
    db.add(fb)
    db.commit()
    return {"message": "Thank you for your feedback! It helps improve FitBuddy."}
