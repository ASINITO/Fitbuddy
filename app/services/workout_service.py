import json
import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import User, WorkoutPlan, WorkoutHistory
from app.services.gemini_service import gemini_service

class WorkoutService:
    @staticmethod
    def create_user_workout_plan(
        db: Session,
        user: User,
        custom_params: Optional[Dict[str, Any]] = None
    ) -> WorkoutPlan:
        """Generate a brand-new 7-day plan with Gemini and store it in database."""
        profile = {
            "age": user.age or 25,
            "weight": user.weight or 70.0,
            "height": user.height or 175.0,
            "fitness_level": custom_params.get("fitness_level") if custom_params and custom_params.get("fitness_level") else (user.fitness_level or "Beginner"),
            "fitness_goal": custom_params.get("goal") if custom_params and custom_params.get("goal") else (user.fitness_goal or "General wellness"),
            "preferred_intensity": custom_params.get("intensity") if custom_params and custom_params.get("intensity") else (user.preferred_intensity or "Moderate"),
            "preferred_duration": custom_params.get("duration") if custom_params and custom_params.get("duration") else (user.preferred_duration or 45),
            "available_days": custom_params.get("available_days") if custom_params and custom_params.get("available_days") else (user.available_days or 4),
            "equipment": custom_params.get("equipment") if custom_params and custom_params.get("equipment") else (user.equipment or "Bodyweight, Dumbbells"),
            "preferences": custom_params.get("preferences") if custom_params and custom_params.get("preferences") else ""
        }

        days_plan = gemini_service.generate_workout_plan(profile)
        
        # Deactivate old active plans
        db.query(WorkoutPlan).filter(
            WorkoutPlan.user_id == user.id,
            WorkoutPlan.is_active == True
        ).update({"is_active": False})

        new_plan = WorkoutPlan(
            user_id=user.id,
            title=f"7-Day {profile['fitness_goal']} Routine",
            goal=profile["fitness_goal"],
            fitness_level=profile["fitness_level"],
            intensity=profile["preferred_intensity"],
            plan_json=json.dumps(days_plan),
            is_active=True,
            version=1
        )
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)

        # Seed initial history rows for each day
        for d in days_plan:
            wh = WorkoutHistory(
                user_id=user.id,
                workout_plan_id=new_plan.id,
                day_number=d.get("day_number", 1),
                focus=d.get("focus", "Workout Day"),
                original_plan_json=json.dumps(d),
                completed=False
            )
            db.add(wh)
        db.commit()

        return new_plan

    @staticmethod
    def adapt_user_workout_plan(
        db: Session,
        user: User,
        plan_id: int,
        feedback: str
    ) -> WorkoutPlan:
        """Modify an existing plan using Gemini AI and preserve versioned history."""
        plan = db.query(WorkoutPlan).filter(
            WorkoutPlan.id == plan_id,
            WorkoutPlan.user_id == user.id
        ).first()

        if not plan:
            raise ValueError("Workout plan not found.")

        current_days = json.loads(plan.plan_json)
        profile = {
            "age": user.age or 25,
            "fitness_level": plan.fitness_level,
            "fitness_goal": plan.goal,
            "preferred_duration": user.preferred_duration or 45
        }

        updated_days = gemini_service.update_workout_plan(current_days, feedback, profile)
        
        # Log to workout history
        wh = WorkoutHistory(
            user_id=user.id,
            workout_plan_id=plan.id,
            day_number=1,
            focus="AI Adaptation: " + feedback[:40],
            original_plan_json=plan.plan_json,
            feedback_text=feedback,
            updated_plan_json=json.dumps(updated_days),
            completed=False
        )
        db.add(wh)

        plan.plan_json = json.dumps(updated_days)
        plan.version += 1
        plan.updated_at = datetime.datetime.utcnow()
        db.commit()
        db.refresh(plan)

        return plan

    @staticmethod
    def mark_day_completed(
        db: Session,
        user_id: int,
        plan_id: int,
        day_number: int,
        completed: bool = True
    ) -> bool:
        """Toggle workout completion status for a specific day."""
        plan = db.query(WorkoutPlan).filter(
            WorkoutPlan.id == plan_id,
            WorkoutPlan.user_id == user_id
        ).first()

        if not plan:
            return False

        days = json.loads(plan.plan_json)
        for d in days:
            if d.get("day_number") == day_number:
                d["completed"] = completed
                break

        plan.plan_json = json.dumps(days)
        
        # Record completion in history
        history_item = db.query(WorkoutHistory).filter(
            WorkoutHistory.user_id == user_id,
            WorkoutHistory.workout_plan_id == plan_id,
            WorkoutHistory.day_number == day_number
        ).first()

        if not history_item:
            history_item = WorkoutHistory(
                user_id=user_id,
                workout_plan_id=plan_id,
                day_number=day_number,
                focus=f"Day {day_number} Workout"
            )
            db.add(history_item)

        history_item.completed = completed
        history_item.completed_at = datetime.datetime.utcnow() if completed else None
        db.commit()

        return True

workout_service = WorkoutService()
