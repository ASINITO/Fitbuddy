from fastapi.testclient import TestClient
from app.main import app
from app.utils.validators import calculate_bmi, estimate_daily_calories

client = TestClient(app)

def test_bmi_calculation():
    # 70 kg, 175 cm -> 70 / (1.75^2) = 22.86 -> Normal weight
    bmi_res = calculate_bmi(height_cm=175.0, weight_kg=70.0)
    assert bmi_res["bmi"] == 22.9
    assert bmi_res["category"] == "Normal weight"
    assert "DISCLAIMER" in bmi_res["disclaimer"]

def test_calorie_estimation():
    # Male 70kg, 175cm, 25yrs, Moderate
    cal_res = estimate_daily_calories(weight_kg=70.0, height_cm=175.0, age=25, gender="Male", activity_level="Moderate")
    assert cal_res["bmr"] > 1400
    assert cal_res["maintenance_calories"] > 2000
    assert "Mifflin-St Jeor" in cal_res["formula_used"]

def test_health_route():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"
