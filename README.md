# FitBuddy – AI-Powered Personalized Fitness, Nutrition & Wellness Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-AI%20Powered-orange.svg)](https://ai.google.dev/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%20%2B%20SQLAlchemy-lightgrey.svg)](https://www.sqlalchemy.org/)

FitBuddy is an intelligent, full-stack fitness and wellness web application designed to act as your personalized digital coach. Powered by Google Gemini AI, FitBuddy continuously learns from user feedback, check-ins, hydration, and sleep logs to generate adaptive workout plans, customized nutrition guides, and multilingual guidance (supporting English and Tamil).

---

## 🌟 Key Features

1. **AI Workout Plan Generator & Continuous Adaptation:**
   - 7-day personalized routines customized to fitness level, equipment, and goals.
   - Dynamic plan adaptation upon natural language feedback (e.g., *"Make workouts easier"*, *"Only 30 minutes"*, *"Add yoga"*).
   - Complete versioned workout history preserving original and updated routines.
2. **AI Nutrition & Meal Guidance:**
   - Macronutrient calculation and meal planning for Vegetarian, Vegan, Non-vegetarian, and Eggetarian diets.
   - Actionable pre-workout and post-workout nutritional strategies.
3. **Multilingual AI Fitness Coach:**
   - Interactive chatbot with support for **English** and **Tamil (தமிழ்)**.
4. **Daily Wellness Check-in & Recovery Advisory:**
   - Input energy levels, muscle soreness, mood, and stress to receive daily Gemini recovery suggestions.
5. **Interactive Biometrics & Health Trackers:**
   - BMI calculation with health classification and medical disclaimer.
   - Mifflin-St Jeor daily caloric expenditure estimation.
   - Water tracking (glasses & ml) with visual progress bars.
   - Sleep duration and quality tracking.
6. **Gamified Achievements & Streak Engine:**
   - Automated badge unlocks (*First Workout*, *3-Day Streak*, *7-Day Streak*, *Hydration Hero*, *Workout Warrior*).
7. **Administrative Dashboard & Analytics:**
   - User distribution analytics by fitness goals and fitness levels via Chart.js.
   - Search and filter registered users without password exposure.
   - Audit trail of user feedback and satisfaction ratings.

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────┐
│                   Frontend Client                      │
│   (HTML5, Tailwind CSS, JavaScript, Jinja2, Chart.js)   │
└───────────────────────────┬────────────────────────────┘
                            │ REST / Session Cookies
┌───────────────────────────▼────────────────────────────┐
│                    FastAPI Backend                     │
│  ├── Auth & Users Router (JWT / Session Security)      │
│  ├── Workout & Exercise Router                         │
│  ├── Nutrition & Progress Router                       │
│  ├── Chatbot Router (Multilingual Support)             │
│  └── Admin & Analytics Router                          │
└─────────────┬───────────────────────────┬──────────────┘
              │                           │
┌─────────────▼─────────────┐ ┌───────────▼──────────────┐
│       Google Gemini       │ │   SQLite + SQLAlchemy    │
│       (gemini-3.8-flash)  │ │  (Persistent Relational  │
│  AI Workout & Chat Engine │ │      Storage Engine)     │
└───────────────────────────┘ └──────────────────────────┘
```

---

## 📁 Project Structure

```
fitbuddy/
├── app/
│   ├── __init__.py
│   ├── config.py              # Environment settings & secrets
│   ├── database.py            # SQLite engine & session management
│   ├── models.py              # SQLAlchemy database models
│   ├── schemas.py             # Pydantic request/response schemas
│   ├── routes/                # Modular API and Web route controllers
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── workout.py
│   │   ├── nutrition.py
│   │   ├── progress.py
│   │   ├── chatbot.py
│   │   └── admin.py
│   ├── services/              # Business logic & AI orchestration
│   │   ├── gemini_service.py
│   │   ├── workout_service.py
│   │   ├── nutrition_service.py
│   │   ├── recommendation_service.py
│   │   └── analytics_service.py
│   └── utils/                 # Security, formulas & streak helpers
│       ├── security.py
│       ├── validators.py
│       └── helpers.py
├── templates/                 # Jinja2 responsive HTML templates
├── static/                    # CSS, JavaScript & client assets
├── tests/                     # Pytest automated test suites
├── seed_database.py           # Demonstration database population script
├── run.py                     # Local application server runner
├── requirements.txt           # Python package dependencies
└── README.md
```

---

## 🚀 Installation & Local Setup

### 1. Prerequisites
- Python 3.10+ installed
- Google Gemini API key (optional for offline testing, as automatic fallback routines are built-in)

### 2. Create and Activate Virtual Environment

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and add your Google Gemini API key:
```env
GEMINI_API_KEY="your_actual_gemini_api_key"
SECRET_KEY="your-secure-secret-key"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="AdminPassword123!"
DATABASE_URL="sqlite:///./fitbuddy.db"
```

### 5. Seed Demonstration Data (Optional but Recommended)
Populate sample users, exercises, and historical workout data:
```bash
python seed_database.py
```

### 6. Run the Application
```bash
uvicorn app.main:app --reload
```
or run with the script:
```bash
python run.py
```

The web application will be accessible at:
👉 **http://127.0.0.1:8000**

Interactive Swagger API Documentation:
👉 **http://127.0.0.1:8000/docs**

---

## 🧪 Automated Testing

Run the pytest suite to verify authentication, calculations, and mocked AI services:
```bash
pytest
```

---

## 🔒 Security & Privacy Practices

- Passwords hashed using standard `bcrypt`.
- Protected routes enforced via session cookies and JWT Bearer authorization.
- Admin APIs require verified `is_admin` privileges.
- User data isolation ensures members can only access their personal health records.
- Input validation enforced at runtime using Pydantic schemas.

---

## ⚠️ Medical & Health Disclaimer

FitBuddy is an educational AI application providing general fitness, exercise explanation, and nutritional suggestions. It does not provide medical diagnoses, treatment plans, or clinical physical therapy. Users should consult a qualified physician or healthcare provider before initiating strenuous exercise.
