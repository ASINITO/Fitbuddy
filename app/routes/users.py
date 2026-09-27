from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserProfileUpdate, BMIResponse, CalorieEstimateResponse
from app.routes.auth import get_current_user
from app.utils.validators import calculate_bmi, estimate_daily_calories

router = APIRouter(tags=["User Profile & Calculations"])

@router.get("/api/profile", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    """Retrieve authenticated user's profile."""
    return current_user

@router.put("/api/profile", response_model=UserResponse)
def update_user_profile(
    profile_in: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's physical stats, preferences, or language."""
    update_data = profile_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(current_user, key, value)
            
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/api/bmi", response_model=BMIResponse)
def get_bmi_calculation(
    height: float = Query(None, description="Height in centimeters"),
    weight: float = Query(None, description="Weight in kilograms"),
    current_user: User = Depends(get_current_user)
):
    """Calculate BMI with category and health disclaimer."""
    h = height if height is not None else current_user.height
    w = weight if weight is not None else current_user.weight
    
    if not h or not w:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Height and weight must be provided or stored in user profile."
        )
    return calculate_bmi(height_cm=h, weight_kg=w)

@router.get("/api/calorie-estimate", response_model=CalorieEstimateResponse)
def get_calorie_estimate(
    current_user: User = Depends(get_current_user)
):
    """Estimate daily caloric requirements using Mifflin-St Jeor formula."""
    if not current_user.height or not current_user.weight or not current_user.age:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Age, height, and weight are required to calculate estimated caloric needs."
        )
    return estimate_daily_calories(
        weight_kg=current_user.weight,
        height_cm=current_user.height,
        age=current_user.age,
        gender=current_user.gender or "Male",
        activity_level=current_user.preferred_intensity or "Moderate"
    )
