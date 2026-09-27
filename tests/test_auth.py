import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import User
from app.utils.security import get_password_hash

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup if needed

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_user_registration_and_login():
    test_username = "pytestuser"
    # Registration
    reg_payload = {
        "full_name": "Test Runner",
        "username": test_username,
        "email": "pytest@example.com",
        "password": "testpassword123",
        "age": 25,
        "fitness_level": "Beginner",
        "fitness_goal": "Strength",
        "dietary_preference": "Vegetarian",
        "preferred_language": "English"
    }
    res_reg = client.post("/api/register", json=reg_payload)
    # 201 Created or 400 if already exists
    assert res_reg.status_code in [201, 400]

    # Login
    login_payload = {
        "username_or_email": test_username,
        "password": "testpassword123"
    }
    res_login = client.post("/api/login", json=login_payload)
    assert res_login.status_code == 200
    assert "access_token" in res_login.json()
