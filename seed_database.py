#!/usr/bin/env python3
"""Seed demonstration data into the FitBuddy database."""
import datetime
import json
from app.database import Base, engine, SessionLocal
from app.models import (
    User, Exercise, Achievement, WorkoutPlan, WorkoutHistory,
    WaterLog, SleepLog, DailyCheckIn, Progress, Feedback
)
from app.utils.security import get_password_hash
from app.services.gemini_service import gemini_service

def seed_all():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    print("Seeding FitBuddy database...")

    try:
        # 1. Admin
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                full_name="Alex Morgan (Coach/Admin)",
                username="admin",
                email="admin@fitbuddy.local",
                hashed_password=get_password_hash("AdminPassword123!"),
                is_admin=True,
                age=32,
                gender="Female",
                height=172.0,
                weight=65.0,
                fitness_level="Advanced",
                fitness_goal="Endurance & Strength",
                preferred_intensity="High",
                preferred_duration=60,
                available_days=5,
                equipment="Full Gym Access",
                dietary_preference="Balanced",
                preferred_language="English"
            )
            db.add(admin)

        # 2. Demo User 1 (Beginner)
        demo_user = db.query(User).filter(User.username == "johndoe").first()
        if not demo_user:
            demo_user = User(
                full_name="John Doe",
                username="johndoe",
                email="john@example.com",
                hashed_password=get_password_hash("password123"),
                is_admin=False,
                age=28,
                gender="Male",
                height=178.0,
                weight=82.5,
                fitness_level="Beginner",
                fitness_goal="Weight management",
                preferred_intensity="Moderate",
                preferred_duration=45,
                available_days=4,
                equipment="Dumbbells, Bodyweight",
                dietary_preference="Vegetarian",
                preferred_language="English"
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)

            # Generate workout plan for demo user
            plan_days = gemini_service.generate_workout_plan({
                "age": demo_user.age,
                "weight": demo_user.weight,
                "height": demo_user.height,
                "fitness_level": demo_user.fitness_level,
                "fitness_goal": demo_user.fitness_goal,
                "preferred_intensity": demo_user.preferred_intensity,
                "preferred_duration": demo_user.preferred_duration,
                "available_days": demo_user.available_days,
                "equipment": demo_user.equipment
            })
            plan_days[0]["completed"] = True
            
            w_plan = WorkoutPlan(
                user_id=demo_user.id,
                title="7-Day Weight Management & Core Routine",
                goal=demo_user.fitness_goal,
                fitness_level=demo_user.fitness_level,
                intensity=demo_user.preferred_intensity,
                plan_json=json.dumps(plan_days),
                is_active=True,
                version=1
            )
            db.add(w_plan)
            db.commit()
            db.refresh(w_plan)

            # History row
            wh = WorkoutHistory(
                user_id=demo_user.id,
                workout_plan_id=w_plan.id,
                day_number=1,
                focus="Upper Body Foundation",
                original_plan_json=json.dumps(plan_days[0]),
                completed=True,
                completed_at=datetime.datetime.utcnow() - datetime.timedelta(hours=2)
            )
            db.add(wh)

            # Progress logs
            for i in range(5, 0, -1):
                p_date = datetime.datetime.utcnow() - datetime.timedelta(days=i * 2)
                p = Progress(
                    user_id=demo_user.id,
                    date=p_date,
                    weight=84.0 - (0.3 * (5 - i)),
                    steps=8500 + (i * 300),
                    running_distance=3.2 + (i * 0.2),
                    waist=92.0 - (0.2 * (5 - i)),
                    notes=f"Week {6 - i} check-in, feeling energized."
                )
                db.add(p)

            # Water and Sleep logs
            for i in range(7):
                day_date = datetime.datetime.utcnow() - datetime.timedelta(days=i)
                wl = WaterLog(
                    user_id=demo_user.id,
                    date=day_date,
                    glasses=8 + (i % 3),
                    amount_ml=2000 + ((i % 3) * 250),
                    daily_target_ml=2500
                )
                sl = SleepLog(
                    user_id=demo_user.id,
                    date=day_date,
                    sleep_time="23:15",
                    wake_time="07:00",
                    duration_hours=7.75 - ((i % 2) * 0.5),
                    sleep_quality="Good" if i % 2 == 0 else "Fair"
                )
                db.add(wl)
                db.add(sl)

            # Daily Check-in
            ci = DailyCheckIn(
                user_id=demo_user.id,
                energy_level=4,
                mood="Energetic",
                sleep_quality="Good",
                muscle_soreness="Mild",
                stress_level=2,
                workout_completed=True,
                water_intake_ml=2250,
                ai_recommendation="Great consistency on Day 1! Keep hydration up and perform 5 mins of hip openers."
            )
            db.add(ci)

            # Feedback
            fb = Feedback(
                user_id=demo_user.id,
                rating=5,
                category="Workouts",
                feedback_text="The AI workout plan adapted perfectly to my home dumbbell setup. Loving the clear instructions!"
            )
            db.add(fb)

        db.commit()
        print("Database seeded successfully with demo users, workouts, logs, and analytics!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_all()
