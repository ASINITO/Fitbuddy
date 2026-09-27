from typing import Dict, Any

def calculate_bmi(height_cm: float, weight_kg: float) -> Dict[str, Any]:
    """Calculate BMI and provide category with health disclaimer."""
    if not height_cm or height_cm <= 0 or not weight_kg or weight_kg <= 0:
        return {
            "bmi": 0.0,
            "category": "Invalid Measurements",
            "health_risk": "N/A",
            "disclaimer": "BMI is a general screening metric and does not constitute medical advice or diagnosis."
        }
    
    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m ** 2), 1)
    
    if bmi < 18.5:
        category = "Underweight"
        risk = "May indicate insufficient nutritional intake or underlying concerns"
    elif 18.5 <= bmi < 25.0:
        category = "Normal weight"
        risk = "Generally associated with lower risk of chronic lifestyle conditions"
    elif 25.0 <= bmi < 30.0:
        category = "Overweight"
        risk = "Increased risk for cardiovascular conditions and metabolic stress"
    else:
        category = "Obesity"
        risk = "Higher risk for hypertension, type 2 diabetes, and joint strain"
        
    return {
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "bmi": bmi,
        "category": category,
        "health_risk": risk,
        "disclaimer": "DISCLAIMER: Body Mass Index (BMI) is an approximate population screening tool. It does not measure body composition, muscle mass, bone density, or overall metabolic health. Always consult a healthcare professional for clinical health evaluations."
    }

def estimate_daily_calories(
    weight_kg: float,
    height_cm: float,
    age: int,
    gender: str = "Male",
    activity_level: str = "Moderate"
) -> Dict[str, Any]:
    """Estimate daily caloric requirements using the Mifflin-St Jeor formula."""
    if not weight_kg or not height_cm or not age:
        return {
            "bmr": 0,
            "maintenance_calories": 0,
            "weight_loss_calories": 0,
            "muscle_gain_calories": 0,
            "formula_used": "Mifflin-St Jeor",
            "disclaimer": "Please provide valid weight, height, and age."
        }
    
    # Basal Metabolic Rate (BMR) via Mifflin-St Jeor equation
    base_bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
    
    g_lower = (gender or "").lower()
    if "female" in g_lower or "woman" in g_lower:
        bmr = base_bmr - 161
    elif "male" in g_lower or "man" in g_lower:
        bmr = base_bmr + 5
    else:
        bmr = base_bmr - 78  # neutral midpoint
    
    # Activity multipliers
    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "high": 1.725,
        "very high": 1.9
    }
    
    mult = multipliers.get(activity_level.lower(), 1.55)
    maintenance = round(bmr * mult)
    loss = round(maintenance - 400)
    gain = round(maintenance + 350)
    
    return {
        "bmr": round(bmr),
        "maintenance_calories": max(1200, maintenance),
        "weight_loss_calories": max(1200, loss),
        "muscle_gain_calories": gain,
        "formula_used": "Mifflin-St Jeor Equation",
        "disclaimer": "DISCLAIMER: Calorie estimations are mathematical approximations based on population statistics. Individual metabolic rate, hormone levels, and daily movement vary. This does NOT replace personalized advice from a registered dietitian or physician."
    }
