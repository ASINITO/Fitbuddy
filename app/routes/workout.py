import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, WorkoutPlan, WorkoutHistory, Exercise
from app.schemas import (
    WorkoutPlanCreate,
    WorkoutPlanAdaptRequest,
    WorkoutPlanResponse,
)
from app.routes.auth import get_current_user
from app.services.workout_service import workout_service
from app.services.gemini_service import gemini_service
from app.utils.helpers import check_and_award_achievements

router = APIRouter(tags=["Workout Plans & Exercises"])

@router.post("/api/workout/generate")
def generate_workout_plan(
    plan_in: Optional[WorkoutPlanCreate] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a personalized 7-day workout plan using Gemini AI."""
    params = plan_in.model_dump(exclude_unset=True) if plan_in else {}
    plan = workout_service.create_user_workout_plan(db, current_user, params)
    
    # Check for first workout plan achievement
    check_and_award_achievements(db, current_user)
    
    return {
        "id": plan.id,
        "title": plan.title,
        "goal": plan.goal,
        "fitness_level": plan.fitness_level,
        "intensity": plan.intensity,
        "version": plan.version,
        "plan": json.loads(plan.plan_json)
    }

@router.post("/api/workout/update")
def adapt_workout_plan(
    adapt_in: WorkoutPlanAdaptRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Adapt existing workout plan based on user feedback using Gemini."""
    try:
        updated_plan = workout_service.adapt_user_workout_plan(
            db=db,
            user=current_user,
            plan_id=adapt_in.plan_id,
            feedback=adapt_in.feedback
        )
        return {
            "id": updated_plan.id,
            "title": updated_plan.title,
            "version": updated_plan.version,
            "plan": json.loads(updated_plan.plan_json),
            "feedback_applied": adapt_in.feedback
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/api/workout/current")
def get_current_workout_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve the user's active workout plan."""
    plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id,
        WorkoutPlan.is_active == True
    ).order_by(WorkoutPlan.created_at.desc()).first()

    if not plan:
        # Auto-generate a plan if user has none
        plan = workout_service.create_user_workout_plan(db, current_user)

    return {
        "id": plan.id,
        "title": plan.title,
        "goal": plan.goal,
        "fitness_level": plan.fitness_level,
        "intensity": plan.intensity,
        "version": plan.version,
        "plan": json.loads(plan.plan_json)
    }

@router.post("/api/workout/complete/{plan_id}/{day_number}")
def toggle_day_completion(
    plan_id: int,
    day_number: int,
    completed: bool = Query(True),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a workout day as completed or incomplete."""
    success = workout_service.mark_day_completed(
        db=db,
        user_id=current_user.id,
        plan_id=plan_id,
        day_number=day_number,
        completed=completed
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
        
    new_badges = check_and_award_achievements(db, current_user)
    return {"success": True, "day_number": day_number, "completed": completed, "new_achievements": new_badges}

@router.get("/api/workout/history")
def get_workout_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get history of all generated plans and adaptations."""
    histories = db.query(WorkoutHistory).filter(
        WorkoutHistory.user_id == current_user.id
    ).order_by(WorkoutHistory.created_at.desc()).limit(30).all()

    return [
        {
            "id": h.id,
            "day_number": h.day_number,
            "focus": h.focus,
            "feedback": h.feedback_text,
            "completed": h.completed,
            "completed_at": h.completed_at.isoformat() if h.completed_at else None,
            "created_at": h.created_at.isoformat()
        }
        for h in histories
    ]

@router.get("/api/exercises")
def list_exercises(
    search: Optional[str] = None,
    muscle_group: Optional[str] = None,
    difficulty: Optional[str] = None,
    equipment: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Search and filter exercise database."""
    query = db.query(Exercise)
    if search:
        query = query.filter(Exercise.name.ilike(f"%{search}%"))
    if muscle_group and muscle_group != "All":
        query = query.filter(Exercise.muscle_group == muscle_group)
    if difficulty and difficulty != "All":
        query = query.filter(Exercise.difficulty == difficulty)
    if equipment and equipment != "All":
        query = query.filter(Exercise.equipment.ilike(f"%{equipment}%"))
        
    exercises = query.order_by(Exercise.name).all()
    return exercises

@router.get("/api/exercises/{exercise_id}")
def get_exercise_details(exercise_id: int, db: Session = Depends(get_db)):
    """Get full details of a specific exercise."""
    ex = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return ex

@router.post("/api/exercises/explain")
def explain_exercise(exercise_name: str = Query(..., description="Name of exercise to explain")):
    """Get AI explanation of form, purpose, mistakes, and safety."""
    return gemini_service.explain_exercise(exercise_name)
