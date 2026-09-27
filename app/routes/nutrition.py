import json
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, NutritionPlan
from app.schemas import NutritionRequest
from app.routes.auth import get_current_user
from app.services.nutrition_service import nutrition_service
from app.services.gemini_service import gemini_service

router = APIRouter(tags=["Nutrition & Meal Plans"])

@router.get("/api/nutrition/plan")
def get_user_nutrition_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve or generate daily nutrition guide."""
    plan = db.query(NutritionPlan).filter(NutritionPlan.user_id == current_user.id).first()
    if not plan:
        plan = nutrition_service.get_or_create_meal_plan(db, current_user)
        
    return {
        "id": plan.id,
        "title": plan.title,
        "dietary_preference": plan.dietary_preference,
        "target_calories": plan.target_calories,
        "plan": json.loads(plan.plan_json),
        "tips": plan.tips
    }

@router.post("/api/nutrition/plan")
def generate_custom_meal_plan(
    req: NutritionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate meal recommendations based on chosen dietary style and calories."""
    plan = nutrition_service.get_or_create_meal_plan(
        db=db,
        user=current_user,
        custom_calories=req.target_calories,
        custom_diet=req.dietary_preference
    )
    return {
        "id": plan.id,
        "title": plan.title,
        "dietary_preference": plan.dietary_preference,
        "target_calories": plan.target_calories,
        "plan": json.loads(plan.plan_json)
    }

@router.post("/api/nutrition/tip")
def get_quick_nutrition_tip(
    goal: Optional[str] = None,
    diet: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Generate quick sports nutrition tip using Gemini."""
    user_goal = goal or current_user.fitness_goal or "General wellness"
    user_diet = diet or current_user.dietary_preference or "Balanced"
    
    prompt = f"Provide a single actionable, science-based daily nutrition tip for a person with goal: '{user_goal}' and diet: '{user_diet}'. Keep it under 2 sentences."
    tip = gemini_service._call_gemini(prompt, "You are a sports nutritionist. No medical diagnosis.")
    
    return {
        "tip": tip.strip() if tip else "Fuel your workouts with complex carbs 1 hour prior and hydrate consistently throughout the day.",
        "goal": user_goal,
        "diet": user_diet
    }
