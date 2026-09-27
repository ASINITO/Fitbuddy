import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import User, NutritionPlan
from app.services.gemini_service import gemini_service
from app.utils.validators import estimate_daily_calories

class NutritionService:
    @staticmethod
    def get_or_create_meal_plan(
        db: Session,
        user: User,
        custom_calories: Optional[int] = None,
        custom_diet: Optional[str] = None
    ) -> NutritionPlan:
        """Create or update daily nutrition recommendations for user."""
        diet = custom_diet or user.dietary_preference or "Vegetarian"
        
        # Calculate target calories if not specified
        if not custom_calories:
            cal_data = estimate_daily_calories(
                weight_kg=user.weight or 70.0,
                height_cm=user.height or 175.0,
                age=user.age or 25,
                gender=user.gender or "Male"
            )
            goal_lower = (user.fitness_goal or "").lower()
            if "loss" in goal_lower or "fat" in goal_lower:
                target_calories = cal_data["weight_loss_calories"]
            elif "muscle" in goal_lower or "strength" in goal_lower:
                target_calories = cal_data["muscle_gain_calories"]
            else:
                target_calories = cal_data["maintenance_calories"]
        else:
            target_calories = custom_calories

        plan_data = gemini_service.generate_meal_plan(
            dietary_pref=diet,
            target_calories=target_calories,
            goal=user.fitness_goal or "General wellness"
        )

        nut_plan = db.query(NutritionPlan).filter(NutritionPlan.user_id == user.id).first()
        if not nut_plan:
            nut_plan = NutritionPlan(
                user_id=user.id,
                title=f"{diet} Nutrition Plan ({target_calories} kcal)",
                dietary_preference=diet,
                target_calories=target_calories,
                plan_json=json.dumps(plan_data),
                tips="Drink water regularly, prioritize protein at every meal, and eat fiber-rich whole foods."
            )
            db.add(nut_plan)
        else:
            nut_plan.dietary_preference = diet
            nut_plan.target_calories = target_calories
            nut_plan.plan_json = json.dumps(plan_data)

        db.commit()
        db.refresh(nut_plan)
        return nut_plan

nutrition_service = NutritionService()
