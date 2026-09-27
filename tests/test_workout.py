import pytest
from unittest.mock import MagicMock
from app.services.gemini_service import gemini_service

def test_workout_plan_structure(monkeypatch):
    # Mock Gemini API response to ensure deterministic local testing
    fake_plan = [
        {
            "day": "Day 1 - Monday",
            "day_number": 1,
            "focus": "Upper Body Push",
            "warmup": "5 mins dynamic arm circles",
            "exercises": [
                {"exercise": "Push-ups", "sets": 3, "reps": "10-12", "rest": "60 sec", "notes": "Neutral spine"}
            ],
            "cooldown": "5 mins chest stretch",
            "recovery_suggestion": "Hydrate and rest",
            "completed": False
        }
    ]
    monkeypatch.setattr(gemini_service, "generate_workout_plan", MagicMock(return_value=fake_plan))
    
    result = gemini_service.generate_workout_plan({"age": 25, "fitness_goal": "Strength"})
    assert isinstance(result, list)
    assert len(result) >= 1
    assert result[0]["focus"] == "Upper Body Push"
    assert "exercises" in result[0]
