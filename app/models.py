import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Fitness profile
    age = Column(Integer, nullable=True)
    gender = Column(String(20), nullable=True)
    height = Column(Float, nullable=True)  # in cm
    weight = Column(Float, nullable=True)  # in kg
    fitness_level = Column(String(30), default="Beginner")  # Beginner, Intermediate, Advanced
    fitness_goal = Column(String(50), default="General wellness")
    preferred_intensity = Column(String(30), default="Moderate")  # Low, Moderate, High
    preferred_duration = Column(Integer, default=45)  # minutes
    available_days = Column(Integer, default=4)  # days/week
    equipment = Column(String(200), default="Bodyweight, Dumbbells")
    dietary_preference = Column(String(50), default="Vegetarian")  # Vegetarian, Non-vegetarian, Vegan, Eggetarian
    preferred_language = Column(String(20), default="English")  # English, Tamil
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    last_active = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    workout_plans = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan")
    workout_histories = relationship("WorkoutHistory", back_populates="user", cascade="all, delete-orphan")
    progress_logs = relationship("Progress", back_populates="user", cascade="all, delete-orphan")
    water_logs = relationship("WaterLog", back_populates="user", cascade="all, delete-orphan")
    sleep_logs = relationship("SleepLog", back_populates="user", cascade="all, delete-orphan")
    daily_checkins = relationship("DailyCheckIn", back_populates="user", cascade="all, delete-orphan")
    user_achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    nutrition_plans = relationship("NutritionPlan", back_populates="user", cascade="all, delete-orphan")


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(150), default="7-Day Personalized AI Workout Plan")
    goal = Column(String(100), nullable=False)
    fitness_level = Column(String(50), nullable=False)
    intensity = Column(String(50), nullable=False)
    plan_json = Column(Text, nullable=False)  # JSON-encoded days and exercises
    is_active = Column(Boolean, default=True)
    version = Column(Integer, default=1)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="workout_plans")
    histories = relationship("WorkoutHistory", back_populates="workout_plan", cascade="all, delete-orphan")


class WorkoutHistory(Base):
    __tablename__ = "workout_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workout_plan_id = Column(Integer, ForeignKey("workout_plans.id"), nullable=True)
    day_number = Column(Integer, default=1)
    focus = Column(String(100), default="Full Body")
    original_plan_json = Column(Text, nullable=True)
    feedback_text = Column(Text, nullable=True)
    updated_plan_json = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="workout_histories")
    workout_plan = relationship("WorkoutPlan", back_populates="histories")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    muscle_group = Column(String(50), index=True, nullable=False)  # Chest, Back, Legs, Shoulders, Arms, Core, Cardio, Flexibility
    difficulty = Column(String(30), nullable=False)  # Beginner, Intermediate, Advanced
    equipment = Column(String(100), default="None")
    description = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    safety_notes = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Progress(Base):
    __tablename__ = "progress_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    weight = Column(Float, nullable=True)
    chest = Column(Float, nullable=True)
    waist = Column(Float, nullable=True)
    arms = Column(Float, nullable=True)
    steps = Column(Integer, nullable=True)
    running_distance = Column(Float, nullable=True)  # km
    strength_record = Column(String(200), nullable=True)  # e.g., "Bench: 80kg, Squat: 100kg"
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="progress_logs")


class WaterLog(Base):
    __tablename__ = "water_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    glasses = Column(Integer, default=0)
    amount_ml = Column(Integer, default=0)
    daily_target_ml = Column(Integer, default=2500)

    user = relationship("User", back_populates="water_logs")


class SleepLog(Base):
    __tablename__ = "sleep_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    sleep_time = Column(String(10), nullable=True)   # e.g. "23:00"
    wake_time = Column(String(10), nullable=True)    # e.g. "07:00"
    duration_hours = Column(Float, default=7.0)
    sleep_quality = Column(String(20), default="Good")  # Poor, Fair, Good, Excellent
    recovery_note = Column(Text, nullable=True)

    user = relationship("User", back_populates="sleep_logs")


class DailyCheckIn(Base):
    __tablename__ = "daily_checkins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    energy_level = Column(Integer, default=3)  # 1-5
    mood = Column(String(30), default="Good")  # Energetic, Calm, Stressed, Tired, Motivated
    sleep_quality = Column(String(30), default="Good")
    muscle_soreness = Column(String(30), default="None")  # None, Mild, Moderate, High
    stress_level = Column(Integer, default=2)  # 1-5
    workout_completed = Column(Boolean, default=False)
    water_intake_ml = Column(Integer, default=2000)
    ai_recommendation = Column(Text, nullable=True)

    user = relationship("User", back_populates="daily_checkins")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    icon = Column(String(50), default="award")
    category = Column(String(50), default="General")
    points = Column(Integer, default=50)

    user_achievements = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    unlocked_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="user_achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sender = Column(String(10), default="user")  # 'user' or 'ai'
    message = Column(Text, nullable=False)
    language = Column(String(10), default="en")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="chat_messages")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1 to 5
    category = Column(String(50), default="General")  # Workouts, Nutrition, AI, UI, Suggestions
    feedback_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="feedbacks")


class NutritionPlan(Base):
    __tablename__ = "nutrition_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(150), default="Daily AI Nutrition Guide")
    dietary_preference = Column(String(50), default="Vegetarian")
    target_calories = Column(Integer, default=2000)
    plan_json = Column(Text, nullable=False)
    tips = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="nutrition_plans")
