import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, engine, get_db, SessionLocal
from app.models import User, Exercise, Achievement
from app.utils.security import get_password_hash
from app.routes.auth import get_current_user_optional, router as auth_router
from app.routes.users import router as users_router
from app.routes.workout import router as workout_router
from app.routes.nutrition import router as nutrition_router
from app.routes.progress import router as progress_router
from app.routes.chatbot import router as chatbot_router
from app.routes.admin import router as admin_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fitbuddy.main")

def init_db_data():
    """Create tables and initialize baseline data."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # 1. Seed Admin User
        admin = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
        if not admin:
            admin = User(
                full_name="System Administrator",
                username=settings.ADMIN_USERNAME,
                email=settings.ADMIN_EMAIL,
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                is_admin=True,
                fitness_level="Advanced",
                fitness_goal="Endurance",
                dietary_preference="Balanced"
            )
            db.add(admin)
            logger.info("Created default administrator account.")

        # 2. Seed Baseline Achievements
        if db.query(Achievement).count() == 0:
            badges = [
                Achievement(code="FIRST_WORKOUT", title="First Workout", description="Completed your very first scheduled workout!", icon="dumbbell", category="Workouts", points=50),
                Achievement(code="STREAK_3", title="3-Day Streak", description="Maintained workout consistency for 3 consecutive days.", icon="flame", category="Streaks", points=100),
                Achievement(code="STREAK_7", title="7-Day Streak", description="A whole week of dedication without missing a beat!", icon="zap", category="Streaks", points=250),
                Achievement(code="HYDRATION_HERO", title="Hydration Hero", description="Reached your daily 2500ml water intake target.", icon="droplet", category="Wellness", points=50),
                Achievement(code="WORKOUT_WARRIOR", title="Workout Warrior", description="Completed 10 total training sessions on FitBuddy.", icon="trophy", category="Milestones", points=300),
                Achievement(code="CONSISTENCY_CHAMPION", title="Consistency Champion", description="Logged 7 daily wellness check-ins.", icon="award", category="Habits", points=200),
            ]
            db.add_all(badges)
            logger.info("Seeded initial achievements.")

        # 3. Seed Baseline Exercises
        if db.query(Exercise).count() == 0:
            sample_exercises = [
                Exercise(
                    name="Standard Push-up",
                    muscle_group="Chest",
                    difficulty="Beginner",
                    equipment="Bodyweight",
                    description="Fundamental horizontal pushing exercise for pectoral and tricep development.",
                    instructions="1. Hands slightly wider than shoulder-width.\n2. Maintain rigid plank from head to heels.\n3. Lower chest to floor and press back up.",
                    safety_notes="Keep elbows at a 45-degree angle to protect shoulder joints."
                ),
                Exercise(
                    name="Goblet Squat",
                    muscle_group="Legs",
                    difficulty="Beginner",
                    equipment="Dumbbell",
                    description="Anteriorly-loaded squat to reinforce upright posture and quadricep strength.",
                    instructions="1. Hold dumbbell vertically against chest.\n2. Stand with feet slightly wider than hips.\n3. Sit back and down between knees.\n4. Drive through mid-foot to stand.",
                    safety_notes="Keep chest tall and avoid rounding the lumbar spine."
                ),
                Exercise(
                    name="Dumbbell Bent-Over Row",
                    muscle_group="Back",
                    difficulty="Intermediate",
                    equipment="Dumbbells",
                    description="Key upper-body pulling motion targeting lats, rhomboids, and rear deltoids.",
                    instructions="1. Hinge forward at the hips to a 45-degree torso angle.\n2. Row weights toward hip crease.\n3. Squeeze shoulder blades together.",
                    safety_notes="Maintain flat neutral spine and do not swing upper body."
                ),
                Exercise(
                    name="Overhead Shoulder Press",
                    muscle_group="Shoulders",
                    difficulty="Intermediate",
                    equipment="Dumbbells",
                    description="Vertical pressing movement developing anterior deltoids and triceps.",
                    instructions="1. Hold dumbbells at shoulder height with palms forward.\n2. Press upward until arms are straight.\n3. Lower with control back to clavicles.",
                    safety_notes="Avoid excessive lumbar arching; brace core tightly."
                ),
                Exercise(
                    name="Plank Hold",
                    muscle_group="Core",
                    difficulty="Beginner",
                    equipment="Bodyweight",
                    description="Isometric core exercise engaging transversus abdominis and glutes.",
                    instructions="1. Rest on forearms and toes.\n2. Squeeze glutes and draw navel toward spine.\n3. Maintain parallel line with floor.",
                    safety_notes="Do not let hips sag or hike toward the ceiling."
                ),
                Exercise(
                    name="Romanian Deadlift",
                    muscle_group="Legs",
                    difficulty="Intermediate",
                    equipment="Dumbbells",
                    description="Hip hinge movement emphasizing hamstrings and gluteus maximus.",
                    instructions="1. Hold weights in front of thighs.\n2. Push hips back while keeping slight knee bend.\n3. Lower weights along shins until hamstring stretch.\n4. Drive hips forward to stand.",
                    safety_notes="Keep back flat; do not round shoulders forward."
                ),
                Exercise(
                    name="Mountain Climbers",
                    muscle_group="Cardio",
                    difficulty="Beginner",
                    equipment="Bodyweight",
                    description="Dynamic cardiovascular drill improving conditioning and core control.",
                    instructions="1. Start in high push-up plank.\n2. Drive knees alternately toward chest.\n3. Maintain rapid, rhythmic cadence.",
                    safety_notes="Keep shoulders directly over wrists and hips level."
                ),
                Exercise(
                    name="World's Greatest Stretch",
                    muscle_group="Flexibility",
                    difficulty="Beginner",
                    equipment="Bodyweight",
                    description="Comprehensive dynamic mobility sequence opening hips, thoracic spine, and ankles.",
                    instructions="1. Step forward into deep lunge.\n2. Place hands on inside of front foot.\n3. Rotate torso and reach arm toward ceiling.\n4. Return and switch sides.",
                    safety_notes="Move smoothly through pain-free range of motion."
                )
            ]
            db.add_all(sample_exercises)
            logger.info("Seeded initial exercise library.")

        db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup:
    init_db_data()
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Static and Templates
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("static/images", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(workout_router)
app.include_router(nutrition_router)
app.include_router(progress_router)
app.include_router(chatbot_router)
app.include_router(admin_router)

# Health endpoint
@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for container monitoring."""
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "gemini_model": settings.GEMINI_MODEL
    }

# Web Template Pages
@app.get("/", response_class=HTMLResponse, tags=["Web Pages"])
def page_index(request: Request, user: User = Depends(get_current_user_optional)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/login", response_class=HTMLResponse, tags=["Web Pages"])
def page_login(request: Request, user: User = Depends(get_current_user_optional)):
    if user:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse("login.html", {"request": request, "user": user})

@app.get("/register", response_class=HTMLResponse, tags=["Web Pages"])
def page_register(request: Request, user: User = Depends(get_current_user_optional)):
    if user:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse("register.html", {"request": request, "user": user})

@app.get("/dashboard", response_class=HTMLResponse, tags=["Web Pages"])
def page_dashboard(request: Request, user: User = Depends(get_current_user_optional)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

@app.get("/workout", response_class=HTMLResponse, tags=["Web Pages"])
def page_workout(request: Request, user: User = Depends(get_current_user_optional)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("workout.html", {"request": request, "user": user})

@app.get("/workout-history", response_class=HTMLResponse, tags=["Web Pages"])
def page_workout_history(request: Request, user: User = Depends(get_current_user_optional)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("workout_history.html", {"request": request, "user": user})

@app.get("/nutrition", response_class=HTMLResponse, tags=["Web Pages"])
def page_nutrition(request: Request, user: User = Depends(get_current_user_optional)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("nutrition.html", {"request": request, "user": user})

@app.get("/progress", response_class=HTMLResponse, tags=["Web Pages"])
def page_progress(request: Request, user: User = Depends(get_current_user_optional)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("progress.html", {"request": request, "user": user})

@app.get("/chatbot", response_class=HTMLResponse, tags=["Web Pages"])
def page_chatbot(request: Request, user: User = Depends(get_current_user_optional)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("chatbot.html", {"request": request, "user": user})

@app.get("/achievements", response_class=HTMLResponse, tags=["Web Pages"])
def page_achievements(request: Request, user: User = Depends(get_current_user_optional)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("achievements.html", {"request": request, "user": user})

@app.get("/profile", response_class=HTMLResponse, tags=["Web Pages"])
def page_profile(request: Request, user: User = Depends(get_current_user_optional)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

@app.get("/settings", response_class=HTMLResponse, tags=["Web Pages"])
def page_settings(request: Request, user: User = Depends(get_current_user_optional)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("settings.html", {"request": request, "user": user})

@app.get("/admin", response_class=HTMLResponse, tags=["Web Pages"])
def page_admin(request: Request, user: User = Depends(get_current_user_optional)):
    if not user or not user.is_admin:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "user": user})

@app.get("/admin/users", response_class=HTMLResponse, tags=["Web Pages"])
def page_admin_users(request: Request, user: User = Depends(get_current_user_optional)):
    if not user or not user.is_admin:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})
