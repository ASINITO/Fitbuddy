import json
import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models import User, DailyCheckIn, WorkoutHistory
from app.services.gemini_service import gemini_service

class RecommendationService:
    @staticmethod
    def generate_recommendation_for_user(db: Session, user: User) -> str:
        """Analyze recent user activity and create an AI wellness recommendation."""
        latest_checkin = db.query(DailyCheckIn).filter(
            DailyCheckIn.user_id == user.id
        ).order_by(DailyCheckIn.date.desc()).first()

        checkin_dict = {
            "energy_level": latest_checkin.energy_level if latest_checkin else 3,
            "mood": latest_checkin.mood if latest_checkin else "Good",
            "sleep_quality": latest_checkin.sleep_quality if latest_checkin else "Good",
            "muscle_soreness": latest_checkin.muscle_soreness if latest_checkin else "None",
            "stress_level": latest_checkin.stress_level if latest_checkin else 2,
            "water_intake_ml": latest_checkin.water_intake_ml if latest_checkin else 2000
        }

        profile = {
            "fitness_goal": user.fitness_goal or "General wellness",
            "fitness_level": user.fitness_level or "Beginner",
            "preferred_intensity": user.preferred_intensity or "Moderate"
        }

        rec = gemini_service.generate_daily_recommendation(checkin_dict, profile)
        
        # Save to check-in if present
        if latest_checkin:
            latest_checkin.ai_recommendation = rec
            db.commit()

        return rec

recommendation_service = RecommendationService()
