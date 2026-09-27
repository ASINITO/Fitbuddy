import datetime
import json
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models import User, WorkoutHistory, DailyCheckIn, WaterLog, Achievement, UserAchievement

def check_and_award_achievements(db: Session, user: User) -> List[str]:
    """Check user activities and unlock badges automatically."""
    newly_unlocked = []
    
    # Get current unlocked achievement IDs
    unlocked_ids = {
        ua.achievement_id for ua in db.query(UserAchievement).filter(UserAchievement.user_id == user.id).all()
    }
    
    all_achievements = {a.code: a for a in db.query(Achievement).all()}
    if not all_achievements:
        return []
    
    # 1. First Workout
    completed_workouts = db.query(WorkoutHistory).filter(
        WorkoutHistory.user_id == user.id,
        WorkoutHistory.completed == True
    ).count()
    
    if completed_workouts >= 1 and "FIRST_WORKOUT" in all_achievements:
        ach = all_achievements["FIRST_WORKOUT"]
        if ach.id not in unlocked_ids:
            db.add(UserAchievement(user_id=user.id, achievement_id=ach.id))
            newly_unlocked.append(ach.title)
            unlocked_ids.add(ach.id)
            
    # 2. 3-Day Streak and 7-Day Streak
    current_streak, _ = calculate_user_streak(db, user.id)
    if current_streak >= 3 and "STREAK_3" in all_achievements:
        ach = all_achievements["STREAK_3"]
        if ach.id not in unlocked_ids:
            db.add(UserAchievement(user_id=user.id, achievement_id=ach.id))
            newly_unlocked.append(ach.title)
            unlocked_ids.add(ach.id)
            
    if current_streak >= 7 and "STREAK_7" in all_achievements:
        ach = all_achievements["STREAK_7"]
        if ach.id not in unlocked_ids:
            db.add(UserAchievement(user_id=user.id, achievement_id=ach.id))
            newly_unlocked.append(ach.title)
            unlocked_ids.add(ach.id)
            
    # 3. Hydration Hero (logged 2500ml+ in a day)
    top_water = db.query(WaterLog).filter(
        WaterLog.user_id == user.id,
        WaterLog.amount_ml >= 2500
    ).first()
    if top_water and "HYDRATION_HERO" in all_achievements:
        ach = all_achievements["HYDRATION_HERO"]
        if ach.id not in unlocked_ids:
            db.add(UserAchievement(user_id=user.id, achievement_id=ach.id))
            newly_unlocked.append(ach.title)
            unlocked_ids.add(ach.id)

    # 4. Workout Warrior (completed 10+ workouts)
    if completed_workouts >= 10 and "WORKOUT_WARRIOR" in all_achievements:
        ach = all_achievements["WORKOUT_WARRIOR"]
        if ach.id not in unlocked_ids:
            db.add(UserAchievement(user_id=user.id, achievement_id=ach.id))
            newly_unlocked.append(ach.title)
            unlocked_ids.add(ach.id)

    # 5. Consistency Champion (7+ daily check-ins)
    checkins_count = db.query(DailyCheckIn).filter(DailyCheckIn.user_id == user.id).count()
    if checkins_count >= 7 and "CONSISTENCY_CHAMPION" in all_achievements:
        ach = all_achievements["CONSISTENCY_CHAMPION"]
        if ach.id not in unlocked_ids:
            db.add(UserAchievement(user_id=user.id, achievement_id=ach.id))
            newly_unlocked.append(ach.title)
            unlocked_ids.add(ach.id)

    if newly_unlocked:
        db.commit()

    return newly_unlocked

def calculate_user_streak(db: Session, user_id: int) -> Tuple[int, int]:
    """Calculate current and longest active streak in days."""
    dates_query = db.query(WorkoutHistory.completed_at).filter(
        WorkoutHistory.user_id == user_id,
        WorkoutHistory.completed == True,
        WorkoutHistory.completed_at != None
    ).order_by(WorkoutHistory.completed_at.desc()).all()
    
    if not dates_query:
        # Fallback check check-in dates
        c_dates = db.query(DailyCheckIn.date).filter(
            DailyCheckIn.user_id == user_id
        ).order_by(DailyCheckIn.date.desc()).all()
        if not c_dates:
            return 0, 0
        dates = sorted({d[0].date() for d in c_dates if d[0]}, reverse=True)
    else:
        dates = sorted({d[0].date() for d in dates_query if d[0]}, reverse=True)
        
    if not dates:
        return 0, 0
        
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    # Check if streak is active (today or yesterday logged)
    if dates[0] == today or dates[0] == yesterday:
        expected = dates[0]
        for d in dates:
            if d == expected:
                current_streak += 1
                expected = expected - datetime.timedelta(days=1)
            else:
                break
    
    # Calculate longest consecutive run
    if len(dates) > 0:
        prev = dates[0]
        temp_streak = 1
        longest_streak = 1
        for d in dates[1:]:
            if (prev - d).days == 1:
                temp_streak += 1
            elif (prev - d).days > 1:
                temp_streak = 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
            prev = d
            
    longest_streak = max(longest_streak, current_streak)
    return current_streak, longest_streak
