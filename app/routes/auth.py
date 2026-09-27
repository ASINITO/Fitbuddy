import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserRegister, UserLogin, UserResponse
from app.utils.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.config import settings

router = APIRouter(tags=["Authentication"])

def get_current_user_optional(request: Request, db: Session = Depends(get_db)) -> User | None:
    """Extract current user from authorization header or cookie, or None."""
    token = None
    # 1. Check Bearer token
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        
    # 2. Check Cookie
    if not token:
        token = request.cookies.get(settings.SESSION_COOKIE_NAME)
        
    if not token:
        return None

    payload = decode_access_token(token)
    if not payload:
        return None

    username = payload.get("sub")
    if not username:
        return None

    user = db.query(User).filter(User.username == username).first()
    return user

def get_current_user(user: User = Depends(get_current_user_optional)) -> User:
    """Require valid authenticated user."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided or have expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_admin(user: User = Depends(get_current_user)) -> User:
    """Require authenticated admin user."""
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required to access this resource."
        )
    return user

@router.post("/api/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserRegister, db: Session = Depends(get_db), response: Response = None):
    """Register a new user account."""
    existing_user = db.query(User).filter(
        (User.username == user_in.username) | (User.email == user_in.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is already registered."
        )

    hashed_pw = get_password_hash(user_in.password)
    user = User(
        full_name=user_in.full_name,
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pw,
        age=user_in.age,
        gender=user_in.gender,
        height=user_in.height,
        weight=user_in.weight,
        fitness_level=user_in.fitness_level or "Beginner",
        fitness_goal=user_in.fitness_goal or "General wellness",
        preferred_intensity=user_in.preferred_intensity or "Moderate",
        preferred_duration=user_in.preferred_duration or 45,
        available_days=user_in.available_days or 4,
        equipment=user_in.equipment or "Bodyweight, Dumbbells",
        dietary_preference=user_in.dietary_preference or "Vegetarian",
        preferred_language=user_in.preferred_language or "English"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Set auth cookie
    token = create_access_token({"sub": user.username, "user_id": user.id, "is_admin": user.is_admin})
    if response:
        response.set_cookie(
            key=settings.SESSION_COOKIE_NAME,
            value=token,
            httponly=True,
            max_age=86400,
            samesite="lax"
        )
    return user

@router.post("/api/login")
def login_user(login_in: UserLogin, db: Session = Depends(get_db), response: Response = None):
    """Authenticate user and return session token."""
    user = db.query(User).filter(
        (User.username == login_in.username_or_email) | (User.email == login_in.username_or_email)
    ).first()

    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Please check your username and password."
        )

    user.last_active = datetime.datetime.utcnow()
    db.commit()

    token = create_access_token({"sub": user.username, "user_id": user.id, "is_admin": user.is_admin})
    if response:
        response.set_cookie(
            key=settings.SESSION_COOKIE_NAME,
            value=token,
            httponly=True,
            max_age=86400,
            samesite="lax"
        )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "is_admin": user.is_admin,
            "fitness_goal": user.fitness_goal,
            "fitness_level": user.fitness_level
        }
    }

@router.post("/api/logout")
def logout_user(response: Response):
    """Log out user and clear session cookie."""
    response.delete_cookie(settings.SESSION_COOKIE_NAME)
    return {"message": "Logged out successfully."}
