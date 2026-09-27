import os
import json
import logging
from typing import Dict, Any, List, Optional
from app.config import settings

logger = logging.getLogger("fitbuddy.gemini")

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        self.model_name = settings.GEMINI_MODEL
        self._client = None
        self._init_client()

    def _init_client(self):
        """Initialize Google GenAI client if API key is present."""
        if self.api_key:
            try:
                from google import genai
                self._client = genai.Client(
                    api_key=self.api_key,
                    http_options={"headers": {"User-Agent": "aistudio-build"}}
                )
                logger.info("Google GenAI client initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize GenAI client: {e}. Fallback heuristics active.")
                self._client = None
        else:
            logger.info("No GEMINI_API_KEY configured. Fallback generator active.")

    def _call_gemini(self, prompt: str, system_instruction: str = "") -> Optional[str]:
        """Centralized caller for Gemini model."""
        if not self._client:
            self._init_client()
        if not self._client:
            return None
        
        try:
            config = {}
            if system_instruction:
                config["system_instruction"] = system_instruction
                
            response = self._client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API invocation failed: {e}")
            return None

    def generate_workout_plan(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate structured 7-day workout plan based on user profile."""
        system_instruction = (
            "You are FitBuddy AI, a certified master fitness coach and exercise physiologist. "
            "Safety rule: Never prescribe dangerous extreme lifts. Provide warm-up, set/rep ranges, "
            "rest periods, cooldown, and recovery guidance for each day. Output strictly valid JSON."
        )
        
        prompt = f"""
USER PROFILE:
- Age: {profile.get('age', 25)}
- Weight: {profile.get('weight', 70)} kg
- Height: {profile.get('height', 175)} cm
- Fitness Level: {profile.get('fitness_level', 'Beginner')}
- Fitness Goal: {profile.get('fitness_goal', 'General wellness')}
- Preferred Intensity: {profile.get('preferred_intensity', 'Moderate')}
- Workout Duration: {profile.get('preferred_duration', 45)} minutes
- Available Days: {profile.get('available_days', 4)} days/week
- Equipment Available: {profile.get('equipment', 'Bodyweight, Dumbbells')}
- Preferences: {profile.get('preferences', 'Balanced routine')}

EXPECTED OUTPUT FORMAT:
Return a strictly valid JSON array of 7 objects (one for each day of the week, Monday through Sunday).
Structure:
[
  {{
    "day": "Day 1 - Monday",
    "day_number": 1,
    "focus": "Upper Body & Core Foundation",
    "warmup": "5-10 mins dynamic arm swings, cat-cow, light shoulder circles",
    "exercises": [
      {{
        "exercise": "Push-ups (or Knee Push-ups)",
        "sets": 3,
        "reps": "8-12",
        "rest": "60 sec",
        "notes": "Keep core tight and elbows at 45 degrees."
      }}
    ],
    "cooldown": "5 mins static chest and lat stretching",
    "recovery_suggestion": "Hydrate with at least 500ml water and ensure 7-8 hours sleep.",
    "completed": false
  }}
]
Include planned active rest days for non-workout days according to available days ({profile.get('available_days', 4)}).
Only return the JSON array, no extra commentary or markdown formatting.
"""
        raw_text = self._call_gemini(prompt, system_instruction)
        if raw_text:
            cleaned = self._clean_json_string(raw_text)
            try:
                parsed = json.loads(cleaned)
                if isinstance(parsed, list) and len(parsed) >= 5:
                    return parsed
            except Exception as e:
                logger.warning(f"Error parsing Gemini workout JSON: {e}")

        # High-quality fallback routine tailored to goal & level
        return self._build_fallback_workout_plan(profile)

    def update_workout_plan(
        self,
        original_plan: List[Dict[str, Any]],
        feedback: str,
        profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Adapt a 7-day workout plan based on user feedback and constraints."""
        system_instruction = (
            "You are FitBuddy AI. You adapt existing fitness routines based on user feedback "
            "such as 'make it easier', 'add more cardio', 'only 30 minutes', or 'add yoga'. "
            "Always preserve good exercise structure and safety. Output strictly valid JSON."
        )

        prompt = f"""
USER FEEDBACK: "{feedback}"

CURRENT WORKOUT PLAN:
{json.dumps(original_plan, indent=2)}

USER PROFILE:
- Level: {profile.get('fitness_level', 'Beginner')}
- Goal: {profile.get('fitness_goal', 'General wellness')}
- Preferred Duration: {profile.get('preferred_duration', 45)} mins

INSTRUCTION:
Modify the 7-day plan directly addressing the user's feedback (e.g. adjust volume, exercise intensity, duration, or rest days).
Return the updated plan as a valid JSON array matching the exact same schema.
"""
        raw_text = self._call_gemini(prompt, system_instruction)
        if raw_text:
            cleaned = self._clean_json_string(raw_text)
            try:
                parsed = json.loads(cleaned)
                if isinstance(parsed, list) and len(parsed) >= 5:
                    return parsed
            except Exception as e:
                logger.warning(f"Error parsing Gemini updated plan JSON: {e}")

        # Programmatic adaptation fallback
        return self._adapt_plan_programmatically(original_plan, feedback)

    def explain_exercise(self, exercise_name: str) -> Dict[str, Any]:
        """Explain proper biomechanics, purpose, mistakes, and safety for an exercise."""
        prompt = f"""
Provide professional exercise instructions for: '{exercise_name}'.
Safety rule: General fitness guidance only. Do not diagnose injuries or joint pathologies.

Format as JSON with keys:
- "name": "{exercise_name}"
- "purpose": short paragraph on primary muscle targets and benefits
- "instructions": list of clear, chronological step-by-step cues
- "common_mistakes": list of 3-4 typical errors to avoid
- "beginner_modification": easier regression for beginners
- "safety_notes": joint protection and posture precautions
"""
        raw = self._call_gemini(prompt, "You are a professional biomechanics coach. Output strict JSON.")
        if raw:
            try:
                cleaned = self._clean_json_string(raw)
                return json.loads(cleaned)
            except Exception:
                pass

        return {
            "name": exercise_name,
            "purpose": f"Builds strength, motor control, and functional stability targeting primary muscle groups for {exercise_name}.",
            "instructions": [
                "Establish a stable stance with feet shoulder-width apart and core engaged.",
                "Inhale and initiate movement with controlled tempo, maintaining a neutral spine.",
                "Reach full safe range of motion without joint locking.",
                "Exhale powerfully as you return to the starting position."
            ],
            "common_mistakes": [
                "Using excessive momentum rather than controlled muscular tension.",
                "Holding your breath under exertion.",
                "Allowing the lower back to round or hyper-extend."
            ],
            "beginner_modification": "Perform with reduced load, supported bodyweight, or reduced range of motion until form is mastered.",
            "safety_notes": "If you experience sharp joint discomfort or pinching, stop immediately. Maintain neutral wrist and spinal alignment."
        }

    def generate_meal_plan(
        self,
        dietary_pref: str,
        target_calories: int,
        goal: str
    ) -> Dict[str, Any]:
        """Generate a structured daily meal structure with estimated macros."""
        prompt = f"""
Generate a healthy, balanced daily meal structure.
Dietary Preference: {dietary_pref}
Approximate Caloric Target: {target_calories} kcal
Primary Goal: {goal}

Output JSON with keys:
- "dietary_preference": "{dietary_pref}"
- "estimated_calories": {target_calories}
- "protein_g": approximate protein grams
- "carbs_g": approximate carbs grams
- "fats_g": approximate fats grams
- "meals": object with "breakfast", "mid_morning", "lunch", "evening_snack", "dinner"
  (each meal should have "name", "description", "calories", "protein")
- "pre_workout": suggestion
- "post_workout": suggestion
- "hydration_tip": suggestion
- "disclaimer": "Nutritional values are mathematical estimates. Consult a registered dietitian for medical dietary regimens."
"""
        raw = self._call_gemini(prompt, "You are an evidence-based sports nutritionist. Output strict JSON.")
        if raw:
            try:
                cleaned = self._clean_json_string(raw)
                return json.loads(cleaned)
            except Exception:
                pass

        # Standard fallback meal plan
        return {
            "dietary_preference": dietary_pref,
            "estimated_calories": target_calories,
            "protein_g": round(target_calories * 0.25 / 4),
            "carbs_g": round(target_calories * 0.50 / 4),
            "fats_g": round(target_calories * 0.25 / 9),
            "meals": {
                "breakfast": {
                    "name": "Power Oatmeal Bowl / Scrambled Eggs",
                    "description": "Rolled oats with chia seeds, banana slices, and protein booster or eggs with whole wheat toast.",
                    "calories": round(target_calories * 0.25),
                    "protein": "25g"
                },
                "mid_morning": {
                    "name": "Fresh Fruit & Handful of Almonds",
                    "description": "Apple or orange with 15 soaked almonds for healthy micronutrients and sustained energy.",
                    "calories": round(target_calories * 0.10),
                    "protein": "6g"
                },
                "lunch": {
                    "name": "Balanced Grain & Protein Plate",
                    "description": "Brown rice or quinoa, grilled paneer/tofu/chicken, mixed steamed greens, and spiced lentils (dal).",
                    "calories": round(target_calories * 0.35),
                    "protein": "35g"
                },
                "evening_snack": {
                    "name": "Greek Yogurt or Roasted Chickpeas",
                    "description": "High-protein snack with cucumber sticks and green tea.",
                    "calories": round(target_calories * 0.10),
                    "protein": "12g"
                },
                "dinner": {
                    "name": "Light Protein Broth & Sautéed Veggies",
                    "description": "Steamed broccoli, carrots, bell peppers with seasoned tofu or grilled fish/chicken breast.",
                    "calories": round(target_calories * 0.20),
                    "protein": "28g"
                }
            },
            "pre_workout": "Banana or a slice of toast with peanut butter 30-45 minutes before training.",
            "post_workout": "Quality protein source with fast-acting carbohydrates within 45-60 minutes.",
            "hydration_tip": "Drink 500ml water 1 hour prior to exercise and sip 150ml every 20 minutes during workouts.",
            "disclaimer": "Nutritional values are mathematical approximations. Do not use for medical dietetic treatment."
        }

    def fitness_chat(
        self,
        message: str,
        profile: Dict[str, Any],
        history: List[Dict[str, str]] = None,
        language: str = "English"
    ) -> str:
        """Interactive fitness coach chatbot supporting English, Tamil, and more."""
        lang_note = "Respond in fluent Tamil (தமிழ்)" if "tamil" in language.lower() else "Respond in clear English"
        
        system_instruction = (
            f"You are FitBuddy AI, a supportive, knowledgeable fitness and wellness assistant. {lang_note}. "
            "Tailor guidance to user's fitness profile. Always maintain safety: "
            "Never diagnose medical conditions or injuries; if the user describes severe pain, chest pain, "
            "or medical symptoms, advise seeing a doctor immediately. Keep responses practical, encouraging, and clear."
        )

        history_context = ""
        if history:
            for item in history[-5:]:
                history_context += f"{item.get('sender', 'user').upper()}: {item.get('message', '')}\n"

        prompt = f"""
USER PROFILE:
- Name: {profile.get('full_name', 'Fitness Enthusiast')}
- Goal: {profile.get('fitness_goal', 'General wellness')}
- Level: {profile.get('fitness_level', 'Beginner')}
- Equipment: {profile.get('equipment', 'Bodyweight')}
- Dietary: {profile.get('dietary_preference', 'Vegetarian')}

RECENT CONVERSATION:
{history_context}

USER MESSAGE:
{message}

COACH RESPONSE ({language}):
"""
        response = self._call_gemini(prompt, system_instruction)
        if response:
            return response.strip()

        if "tamil" in language.lower():
            return f"வணக்கம்! உங்கள் உடற்பயிற்சி இலக்கு: {profile.get('fitness_goal', 'ஆரோக்கியம்')}. உடற்பயிற்சிக்கு முன் போதுமான தண்ணீர் குடியுங்கள், மற்றும் சரியான முறையில் பயிற்சி செய்யுங்கள். நான் உங்களுக்கு எப்படி உதவ முடியும்?"
        return (
            f"Hello {profile.get('full_name', 'there')}! As your FitBuddy coach, I'm here to support your "
            f"journey towards '{profile.get('fitness_goal', 'better fitness')}'. Remember to stay hydrated, "
            "maintain progressive overload safely, and listen to your body. What would you like to focus on today?"
        )

    def generate_daily_recommendation(
        self,
        checkin: Dict[str, Any],
        profile: Dict[str, Any]
    ) -> str:
        """Generate smart daily recovery/workout adaptation based on check-in stats."""
        prompt = f"""
Generate a concise 2-3 sentence personalized wellness coaching recommendation.
Today's Check-in:
- Energy Level: {checkin.get('energy_level', 3)} / 5
- Mood: {checkin.get('mood', 'Good')}
- Sleep Quality: {checkin.get('sleep_quality', 'Good')}
- Muscle Soreness: {checkin.get('muscle_soreness', 'None')}
- Stress Level: {checkin.get('stress_level', 2)} / 5
- Water Intake: {checkin.get('water_intake_ml', 2000)} ml

User Goal: {profile.get('fitness_goal', 'General wellness')}
User Fitness Level: {profile.get('fitness_level', 'Beginner')}

Safety rule: Do not diagnose medical conditions. Provide actionable training, recovery, and hydration advice.
"""
        rec = self._call_gemini(prompt, "You are a professional wellness coach.")
        if rec:
            return rec.strip()

        # Heuristic fallback based on soreness and energy
        soreness = str(checkin.get("muscle_soreness", "None")).lower()
        energy = int(checkin.get("energy_level", 3))
        
        if "high" in soreness or energy <= 2:
            return (
                "Your recovery markers show fatigue and muscle soreness. Prioritize an active recovery day "
                "with gentle 20-minute walking, foam rolling, and an extra 500ml of electrolyte hydration before bed."
            )
        elif energy >= 4 and soreness in ["none", "mild"]:
            return (
                "Your energy and readiness are primed today! Great time to hit your key compound lifts with full focus "
                "or push the intensity on your workout session."
            )
        else:
            return (
                "Steady consistency is key. Keep your hydration target on track and complete your scheduled routine "
                "with deliberate warm-up and post-workout static stretches."
            )

    def _clean_json_string(self, text: str) -> str:
        """Strip markdown fences from model response."""
        cleaned = text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        return cleaned.strip()

    def _build_fallback_workout_plan(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Deterministic, well-structured 7-day routine when offline."""
        level = profile.get("fitness_level", "Beginner")
        goal = profile.get("fitness_goal", "General wellness")
        
        return [
            {
                "day": "Day 1 - Monday",
                "day_number": 1,
                "focus": "Upper Body Strength & Posture",
                "warmup": "6 mins dynamic arm circles, cat-cow, band pull-aparts",
                "exercises": [
                    {"exercise": "Standard / Incline Push-ups", "sets": 3, "reps": "8-12", "rest": "60 sec", "notes": "Engage core, smooth tempo"},
                    {"exercise": "Dumbbell Bent-Over Row", "sets": 3, "reps": "10-12", "rest": "60 sec", "notes": "Squeeze lats at the top"},
                    {"exercise": "Overhead Shoulder Press", "sets": 3, "reps": "10", "rest": "60 sec", "notes": "Keep ribs tucked down"},
                    {"exercise": "Plank Hold", "sets": 3, "reps": "30-45 sec", "rest": "45 sec", "notes": "Straight line from heels to crown"}
                ],
                "cooldown": "5 mins shoulder and chest wall stretches",
                "recovery_suggestion": "Post-workout hydration with 500ml water and protein snack.",
                "completed": False
            },
            {
                "day": "Day 2 - Tuesday",
                "day_number": 2,
                "focus": "Lower Body Power & Mobility",
                "warmup": "6 mins bodyweight hip openers, leg swings, glute bridges",
                "exercises": [
                    {"exercise": "Bodyweight / Goblet Squats", "sets": 3, "reps": "12-15", "rest": "60 sec", "notes": "Keep chest proud and knees tracking toes"},
                    {"exercise": "Reverse Lunges", "sets": 3, "reps": "10 each leg", "rest": "60 sec", "notes": "Lower under control without knee banging"},
                    {"exercise": "Romanian Deadlifts (Dumbbells)", "sets": 3, "reps": "10-12", "rest": "75 sec", "notes": "Hinge at hips with flat back"},
                    {"exercise": "Standing Calf Raises", "sets": 3, "reps": "15-20", "rest": "45 sec", "notes": "Full extension at the top"}
                ],
                "cooldown": "5 mins hamstring and hip flexor stretches",
                "recovery_suggestion": "Warm shower and gentle lower body foam rolling.",
                "completed": False
            },
            {
                "day": "Day 3 - Wednesday",
                "day_number": 3,
                "focus": "Active Recovery & Core Stability",
                "warmup": "5 mins deep breathing and light walking",
                "exercises": [
                    {"exercise": "Bird-Dog Extensions", "sets": 3, "reps": "10 each side", "rest": "30 sec", "notes": "Maintain stable lumbar spine"},
                    {"exercise": "Side Plank Hold", "sets": 2, "reps": "25 sec each side", "rest": "45 sec", "notes": "Elevate hips high"},
                    {"exercise": "Brisk Outdoor Walk / Light Cycling", "sets": 1, "reps": "25 mins", "rest": "N/A", "notes": "Conversational zone 2 pace"}
                ],
                "cooldown": "8 mins full body yoga flow (child's pose, cobra, downward dog)",
                "recovery_suggestion": "Focus on high-quality sleep and 2.5L hydration today.",
                "completed": False
            },
            {
                "day": "Day 4 - Thursday",
                "day_number": 4,
                "focus": "Upper Body Pull & Arms",
                "warmup": "5 mins thoracic rotations and jumping jacks",
                "exercises": [
                    {"exercise": "Resistance Band / Lat Pulldown", "sets": 3, "reps": "12", "rest": "60 sec", "notes": "Pull elbows down towards pockets"},
                    {"exercise": "Bicep Dumbbell Curls", "sets": 3, "reps": "10-12", "rest": "45 sec", "notes": "Strict form without swinging torso"},
                    {"exercise": "Tricep Overhead Extension / Dips", "sets": 3, "reps": "12", "rest": "45 sec", "notes": "Keep upper arms stable"},
                    {"exercise": "Face Pulls", "sets": 3, "reps": "15", "rest": "45 sec", "notes": "Strengthen rear delts and rotator cuffs"}
                ],
                "cooldown": "5 mins upper back and tricep stretches",
                "recovery_suggestion": "Replenish with complex carbs and lean protein.",
                "completed": False
            },
            {
                "day": "Day 5 - Friday",
                "day_number": 5,
                "focus": "Full Body Conditioning & Cardio",
                "warmup": "6 mins high knees, butt kicks, arm sweeps",
                "exercises": [
                    {"exercise": "Kettlebell / Dumbbell Swings", "sets": 3, "reps": "15", "rest": "60 sec", "notes": "Explosive hip snap, not a squat"},
                    {"exercise": "Push-up to Downward Dog", "sets": 3, "reps": "8-10", "rest": "45 sec", "notes": "Combines pushing with shoulder mobility"},
                    {"exercise": "Mountain Climbers", "sets": 3, "reps": "30 sec", "rest": "45 sec", "notes": "Maintain neutral spine"},
                    {"exercise": "Jumping Rope or High Knees", "sets": 3, "reps": "60 sec", "rest": "60 sec", "notes": "Cardiovascular endurance interval"}
                ],
                "cooldown": "6 mins full body cool down walk and deep breathing",
                "recovery_suggestion": "Magnesium-rich dinner and optimal 8-hour sleep.",
                "completed": False
            },
            {
                "day": "Day 6 - Saturday",
                "day_number": 6,
                "focus": "Functional Mobility & Flexibility Flow",
                "warmup": "3 mins gentle neck and spine rolls",
                "exercises": [
                    {"exercise": "World's Greatest Stretch", "sets": 2, "reps": "5 each side", "rest": "30 sec", "notes": "Unlocks hips, thoracic, and ankles"},
                    {"exercise": "Deep Squat Pry & Hold", "sets": 2, "reps": "45 sec", "rest": "30 sec", "notes": "Open up adductors and ankles"},
                    {"exercise": "Dead Hang from Pull-up Bar", "sets": 3, "reps": "20-30 sec", "rest": "45 sec", "notes": "Decompresses spinal vertebrae"}
                ],
                "cooldown": "10 mins mindfulness meditation and lying hamstring stretches",
                "recovery_suggestion": "Enjoy an outdoor nature walk or relaxing activity.",
                "completed": False
            },
            {
                "day": "Day 7 - Sunday",
                "day_number": 7,
                "focus": "Complete Rest & Mental Reset",
                "warmup": "None required",
                "exercises": [
                    {"exercise": "Restorative Rest Day", "sets": 1, "reps": "All day", "rest": "N/A", "notes": "Allow muscular tissue and nervous system full recovery"}
                ],
                "cooldown": "Optional evening light walk and gentle stretching",
                "recovery_suggestion": "Meal prep healthy balanced foods for the upcoming week.",
                "completed": False
            }
        ]

    def _adapt_plan_programmatically(
        self,
        original_plan: List[Dict[str, Any]],
        feedback: str
    ) -> List[Dict[str, Any]]:
        """Programmatic adaptation if AI network call is unavailable."""
        f_lower = feedback.lower()
        adapted = json.loads(json.dumps(original_plan))
        
        for day in adapted:
            exercises = day.get("exercises", [])
            if "easier" in f_lower or "less" in f_lower:
                for ex in exercises:
                    ex["sets"] = max(2, ex.get("sets", 3) - 1)
                    ex["rest"] = "90 sec"
                day["recovery_suggestion"] += " (Adapted: Lowered volume for gentler intensity)."
            elif "30" in f_lower or "short" in f_lower:
                day["exercises"] = exercises[:3]
                day["warmup"] = "3-4 mins quick dynamic mobility"
                day["cooldown"] = "3 mins express stretch"
                day["recovery_suggestion"] += " (Adapted: Condensed 30-min express format)."
            elif "cardio" in f_lower:
                day["exercises"].append({
                    "exercise": "Cardio Burn Finisher (Jumping Jacks / Shadow Boxing)",
                    "sets": 3,
                    "reps": "45 sec",
                    "rest": "30 sec",
                    "notes": "Added per your request for extra cardio stimulus"
                })
            elif "yoga" in f_lower or "stretch" in f_lower:
                day["cooldown"] = "10 mins relaxing restorative yoga flow"
                
        return adapted

gemini_service = GeminiService()
