from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User, WorkoutPlan, WorkoutHistory, Feedback, DailyCheckIn

class AnalyticsService:
    @staticmethod
    def get_admin_metrics(db: Session) -> Dict[str, Any]:
        """Aggregate platform statistics for admin dashboard."""
        total_users = db.query(User).count()
        total_plans = db.query(WorkoutPlan).count()
        total_adaptations = db.query(WorkoutHistory).filter(WorkoutHistory.feedback_text != None).count()
        total_completed_workouts = db.query(WorkoutHistory).filter(WorkoutHistory.completed == True).count()
        total_feedback = db.query(Feedback).count()
        
        # Breakdown by fitness goal
        goal_counts = db.query(User.fitness_goal, func.count(User.id)).group_by(User.fitness_goal).all()
        goals_data = {g or "Unspecified": count for g, count in goal_counts}
        
        # Breakdown by fitness level
        level_counts = db.query(User.fitness_level, func.count(User.id)).group_by(User.fitness_level).all()
        levels_data = {lvl or "Unspecified": count for lvl, count in level_counts}
        
        # Recent feedbacks
        feedbacks = db.query(Feedback).order_by(Feedback.created_at.desc()).limit(10).all()
        
        return {
            "total_users": total_users,
            "active_users": max(1, total_users),
            "workout_plans_generated": total_plans,
            "updated_plans": total_adaptations,
            "completed_workouts": total_completed_workouts,
            "feedback_count": total_feedback,
            "goals_breakdown": goals_data,
            "levels_breakdown": levels_data,
            "recent_feedbacks": feedbacks
        }

analytics_service = AnalyticsService()
