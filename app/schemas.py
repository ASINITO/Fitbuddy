import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    age: Optional[int] = Field(None, ge=10, le=120)
    gender: Optional[str] = "Prefer not to say"
    height: Optional[float] = Field(None, ge=50, le=280)  # cm
    weight: Optional[float] = Field(None, ge=20, le=400)  # kg
    fitness_level: Optional[str] = "Beginner"  # Beginner, Intermediate, Advanced
    fitness_goal: Optional[str] = "General wellness"
    preferred_intensity: Optional[str] = "Moderate"
    preferred_duration: Optional[int] = 45
    available_days: Optional[int] = 4
    equipment: Optional[str] = "Bodyweight, Dumbbells"
    dietary_preference: Optional[str] = "Vegetarian"
    preferred_language: Optional[str] = "English"

class UserLogin(BaseModel):
    username_or_email: str
    password: str

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    fitness_goal: Optional[str] = None
    fitness_level: Optional[str] = None
    preferred_intensity: Optional[str] = None
    preferred_duration: Optional[int] = None
    available_days: Optional[int] = None
    equipment: Optional[str] = None
    dietary_preference: Optional[str] = None
    preferred_language: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
    is_admin: bool
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    fitness_level: Optional[str] = None
    fitness_goal: Optional[str] = None
    preferred_intensity: Optional[str] = None
    preferred_duration: Optional[int] = None
    available_days: Optional[int] = None
    equipment: Optional[str] = None
    dietary_preference: Optional[str] = None
    preferred_language: Optional[str] = None
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# Workout schemas
class ExerciseDetail(BaseModel):
    exercise: str
    sets: int
    reps: str
    rest: str
    notes: Optional[str] = ""

class WorkoutDay(BaseModel):
    day: str
    day_number: int
    focus: str
    warmup: str
    exercises: List[ExerciseDetail]
    cooldown: str
    recovery_suggestion: str
    completed: Optional[bool] = False

class WorkoutPlanCreate(BaseModel):
    goal: Optional[str] = None
    fitness_level: Optional[str] = None
    intensity: Optional[str] = None
    duration: Optional[int] = None
    available_days: Optional[int] = None
    equipment: Optional[str] = None
    preferences: Optional[str] = None

class WorkoutPlanAdaptRequest(BaseModel):
    plan_id: int
    feedback: str

class WorkoutPlanResponse(BaseModel):
    id: int
    user_id: int
    title: str
    goal: str
    fitness_level: str
    intensity: str
    plan_json: str
    version: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# Progress schemas
class ProgressCreate(BaseModel):
    weight: Optional[float] = None
    chest: Optional[float] = None
    waist: Optional[float] = None
    arms: Optional[float] = None
    steps: Optional[int] = None
    running_distance: Optional[float] = None
    strength_record: Optional[str] = None
    notes: Optional[str] = None

class WaterLogCreate(BaseModel):
    glasses: int = Field(..., ge=0)
    amount_ml: int = Field(..., ge=0)
    daily_target_ml: Optional[int] = 2500

class SleepLogCreate(BaseModel):
    sleep_time: Optional[str] = "23:00"
    wake_time: Optional[str] = "07:00"
    duration_hours: float = Field(..., ge=0, le=24)
    sleep_quality: str = "Good"
    recovery_note: Optional[str] = None

class DailyCheckInCreate(BaseModel):
    energy_level: int = Field(3, ge=1, le=5)
    mood: str = "Good"
    sleep_quality: str = "Good"
    muscle_soreness: str = "None"
    stress_level: int = Field(2, ge=1, le=5)
    workout_completed: bool = False
    water_intake_ml: int = 2000

class ChatMessageCreate(BaseModel):
    message: str = Field(..., min_length=1)
    language: Optional[str] = "English"

class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    category: str = "General"
    feedback_text: str = Field(..., min_length=2)

class NutritionRequest(BaseModel):
    dietary_preference: Optional[str] = "Vegetarian"
    target_calories: Optional[int] = 2000
    goal: Optional[str] = "General wellness"

class BMIResponse(BaseModel):
    height_cm: float
    weight_kg: float
    bmi: float
    category: str
    health_risk: str
    disclaimer: str

class CalorieEstimateResponse(BaseModel):
    bmr: float
    maintenance_calories: float
    weight_loss_calories: float
    muscle_gain_calories: float
    formula_used: str
    disclaimer: str
