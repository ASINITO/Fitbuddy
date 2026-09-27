import { UserProfile, ExerciseItem, WorkoutPlan, AchievementBadge, NutritionPlan } from './types';

export const initialUser: UserProfile = {
  id: 1,
  fullName: "Alex Rivera",
  username: "alexrivera",
  email: "alex@fitbuddy.local",
  isAdmin: true,
  age: 27,
  gender: "Male",
  height: 178, // cm
  weight: 76.5, // kg
  fitnessGoal: "Muscle building & Wellness",
  fitnessLevel: "Intermediate",
  preferredIntensity: "Moderate",
  preferredDuration: 45,
  availableDays: 4,
  equipment: "Dumbbells, Bodyweight, Resistance Bands",
  dietaryPreference: "Vegetarian",
  preferredLanguage: "English",
  createdAt: "2026-09-01"
};

export const initialExercises: ExerciseItem[] = [
  {
    id: 1,
    name: "Standard Push-up",
    muscleGroup: "Chest",
    difficulty: "Beginner",
    equipment: "Bodyweight",
    description: "Foundational upper-body horizontal pressing movement.",
    instructions: [
      "Place hands flat on the floor, slightly wider than shoulder-width.",
      "Engage glutes and core to form a straight line from heels to crown.",
      "Lower chest until elbows hit a 90-degree angle, keeping elbows tucked at 45 degrees.",
      "Press through palms to return to the starting position."
    ],
    safetyNotes: "Avoid flaring elbows perpendicular to torso to prevent shoulder impingement."
  },
  {
    id: 2,
    name: "Goblet Squat",
    muscleGroup: "Legs",
    difficulty: "Beginner",
    equipment: "Dumbbell",
    description: "Anteriorly loaded compound movement that reinforces upright spinal posture.",
    instructions: [
      "Hold a dumbbell vertically against your sternum with both hands.",
      "Set feet slightly outside hip-width with toes turned slightly outward.",
      "Initiate by sitting back and down between knees, keeping chest proud.",
      "Descend until thighs are parallel to ground, then drive through mid-foot to stand."
    ],
    safetyNotes: "Do not let knees collapse inward during descent or ascent."
  },
  {
    id: 3,
    name: "Dumbbell Romanian Deadlift",
    muscleGroup: "Legs",
    difficulty: "Intermediate",
    equipment: "Dumbbells",
    description: "Posterior-chain hinge targeting hamstrings, gluteus maximus, and erector spinae.",
    instructions: [
      "Stand tall holding dumbbells against fronts of thighs.",
      "Maintain a soft knee bend and push hips directly backward.",
      "Lower dumbbells along shins while maintaining a completely neutral spine.",
      "Squeeze glutes and extend hips forward to return to standing."
    ],
    safetyNotes: "Avoid rounding the upper or lower back. If you feel lower back strain, stop earlier."
  },
  {
    id: 4,
    name: "Dumbbell Bent-Over Row",
    muscleGroup: "Back",
    difficulty: "Intermediate",
    equipment: "Dumbbells",
    description: "Essential horizontal pull targeting latissimus dorsi, rhomboids, and rear deltoids.",
    instructions: [
      "Hinge forward at 45 degrees with flat back and knees softly bent.",
      "Pull dumbbells towards hip crease while leading with elbows.",
      "Pause for a brief contraction at the top, squeezing shoulder blades.",
      "Lower with controlled tempo back to full arm extension."
    ],
    safetyNotes: "Brace core tightly and refrain from jerking weights with spinal momentum."
  },
  {
    id: 5,
    name: "Overhead Dumbbell Press",
    muscleGroup: "Shoulders",
    difficulty: "Intermediate",
    equipment: "Dumbbells",
    description: "Vertical pressing movement developing anterior deltoids and triceps.",
    instructions: [
      "Hold dumbbells at shoulder height with palms facing forward.",
      "Press dumbbells directly upward until arms are fully extended overhead.",
      "Avoid locking elbows harshly at the apex.",
      "Lower smoothly back to clavicle level."
    ],
    safetyNotes: "Keep ribcage pinned down and core engaged to prevent hyperextending lumbar spine."
  },
  {
    id: 6,
    name: "Plank Hold",
    muscleGroup: "Core",
    difficulty: "Beginner",
    equipment: "Bodyweight",
    description: "Isometric anti-extension core stability exercise.",
    instructions: [
      "Support weight on forearms and toes with elbows directly below shoulders.",
      "Tuck pelvis slightly (posterior tilt) and contract glutes firmly.",
      "Breathe rhythmically while holding position for time."
    ],
    safetyNotes: "Do not let hips sag toward the ground or pike excessively into an inverted V."
  },
  {
    id: 7,
    name: "Dumbbell Bicep Curls",
    muscleGroup: "Arms",
    difficulty: "Beginner",
    equipment: "Dumbbells",
    description: "Isolation movement developing bicep brachii and brachialis.",
    instructions: [
      "Stand tall with dumbbells at sides, palms facing forward.",
      "Keep elbows pinned to ribcage as you curl weights toward shoulders.",
      "Squeeze biceps at peak contraction, then lower under 2-second control."
    ],
    safetyNotes: "Eliminate body sway and hip swinging to ensure tension stays purely on biceps."
  },
  {
    id: 8,
    name: "Bench / Chair Tricep Dips",
    muscleGroup: "Arms",
    difficulty: "Beginner",
    equipment: "Bodyweight",
    description: "Bodyweight pushing exercise targeting all three heads of the triceps.",
    instructions: [
      "Sit on edge of sturdy chair or bench, hands gripping edge beside hips.",
      "Slide hips forward off bench with knees bent 90 degrees.",
      "Lower torso by bending elbows until upper arms are parallel to floor.",
      "Drive through palms to return to top."
    ],
    safetyNotes: "Keep back close to the bench to avoid excessive anterior shoulder strain."
  },
  {
    id: 9,
    name: "Mountain Climbers",
    muscleGroup: "Cardio",
    difficulty: "Beginner",
    equipment: "Bodyweight",
    description: "High-cadence conditioning drill boosting cardiovascular capacity and core stability.",
    instructions: [
      "Start in standard high push-up plank with hands under shoulders.",
      "Drive right knee towards chest, then quickly switch to left knee.",
      "Maintain a rapid, rhythmic running motion while keeping hips level."
    ],
    safetyNotes: "Avoid bounding hips up and down; keep shoulder blades protracted and stable."
  },
  {
    id: 10,
    name: "World's Greatest Stretch",
    muscleGroup: "Flexibility",
    difficulty: "Beginner",
    equipment: "Bodyweight",
    description: "Multi-joint dynamic mobility drill opening thoracic spine, hips, and hamstrings.",
    instructions: [
      "Step forward into a deep lunge position with hands placed inside front foot.",
      "Drop inside elbow toward instep for an adductor stretch.",
      "Rotate torso toward front knee and extend top arm toward the sky.",
      "Hold for 3 seconds, lower hand, and sit hips back to stretch front hamstring."
    ],
    safetyNotes: "Move smoothly through active ranges of motion; never force a painful stretch."
  }
];

export const initialBadges: AchievementBadge[] = [
  {
    id: "first_workout",
    title: "First Workout",
    description: "Completed your first scheduled training session on FitBuddy!",
    icon: "dumbbell",
    category: "Workouts",
    points: 50,
    unlocked: true,
    unlockedAt: "Sep 20, 2026"
  },
  {
    id: "streak_3",
    title: "3-Day Streak",
    description: "Maintained workout consistency for 3 consecutive days.",
    icon: "flame",
    category: "Streaks",
    points: 100,
    unlocked: true,
    unlockedAt: "Sep 23, 2026"
  },
  {
    id: "streak_7",
    title: "7-Day Streak",
    description: "A full week of non-stop dedication to your wellness goals!",
    icon: "zap",
    category: "Streaks",
    points: 250,
    unlocked: false
  },
  {
    id: "hydration_hero",
    title: "Hydration Hero",
    description: "Drank at least 2500ml of water in a single day.",
    icon: "droplet",
    category: "Wellness",
    points: 50,
    unlocked: true,
    unlockedAt: "Sep 25, 2026"
  },
  {
    id: "workout_warrior",
    title: "Workout Warrior",
    description: "Completed 10 total guided training sessions.",
    icon: "trophy",
    category: "Milestones",
    points: 300,
    unlocked: false
  },
  {
    id: "consistency_champion",
    title: "Consistency Champion",
    description: "Logged 7 daily wellness check-ins.",
    icon: "award",
    category: "Habits",
    points: 200,
    unlocked: false
  }
];

export const initialPlan: WorkoutPlan = {
  id: 101,
  title: "7-Day Functional Muscle & Wellness Routine",
  goal: "Muscle building & Wellness",
  fitnessLevel: "Intermediate",
  intensity: "Moderate",
  version: 1,
  createdAt: "2026-09-24",
  days: [
    {
      day: "Monday",
      dayNumber: 1,
      focus: "Upper Body Hypertrophy & Posture",
      warmup: "6 mins dynamic shoulder dislocates, cat-cow, and band pull-aparts",
      exercises: [
        { exercise: "Standard Push-up", sets: 3, reps: "10-12", rest: "60 sec", notes: "Elbows at 45 degrees, rigid core" },
        { exercise: "Dumbbell Bent-Over Row", sets: 3, reps: "10-12", rest: "60 sec", notes: "Squeeze shoulder blades together" },
        { exercise: "Overhead Dumbbell Press", sets: 3, reps: "10", rest: "75 sec", notes: "Full lock-out overhead without arching back" },
        { exercise: "Dumbbell Bicep Curls", sets: 3, reps: "12", rest: "45 sec", notes: "Controlled eccentric lowering" },
        { exercise: "Plank Hold", sets: 3, reps: "45 sec", rest: "45 sec", notes: "Tuck pelvis and brace core" }
      ],
      cooldown: "5 mins static chest doorway stretch and seated spinal twists",
      recoverySuggestion: "Consume 30g protein within 1 hour and hydrate with 600ml water.",
      completed: true
    },
    {
      day: "Tuesday",
      dayNumber: 2,
      focus: "Lower Body Power & Posterior Chain",
      warmup: "6 mins hip 90/90 openers, bodyweight glute bridges, leg swings",
      exercises: [
        { exercise: "Goblet Squat", sets: 4, reps: "10-12", rest: "75 sec", notes: "Deep upright squat driving knees out" },
        { exercise: "Dumbbell Romanian Deadlift", sets: 3, reps: "10-12", rest: "75 sec", notes: "Hinge deep at hips with flat back" },
        { exercise: "Reverse Lunges", sets: 3, reps: "10 each leg", rest: "60 sec", notes: "Step back softly without knee slamming" },
        { exercise: "Standing Calf Raises", sets: 3, reps: "15-20", rest: "45 sec", notes: "2-second pause at top extension" }
      ],
      cooldown: "5 mins kneeling hip flexor stretch and standing quad stretches",
      recoverySuggestion: "Warm evening epsom salt bath and gentle leg foam rolling.",
      completed: true
    },
    {
      day: "Wednesday",
      dayNumber: 3,
      focus: "Active Recovery & Mobility Flow",
      warmup: "4 mins diaphragmatic box breathing and wrist rolls",
      exercises: [
        { exercise: "World's Greatest Stretch", sets: 2, reps: "5 each side", rest: "30 sec", notes: "Breathe through the twist" },
        { exercise: "Bird-Dog Extensions", sets: 3, reps: "10 each side", rest: "30 sec", notes: "Extend opposite arm and leg smoothly" },
        { exercise: "Brisk Outdoor Zone 2 Walk", sets: 1, reps: "30 mins", rest: "N/A", notes: "Light conversational aerobic pace" }
      ],
      cooldown: "6 mins child's pose and downward dog pedal",
      recoverySuggestion: "Prioritize 8+ hours uninterrupted sleep tonight.",
      completed: false
    },
    {
      day: "Thursday",
      dayNumber: 4,
      focus: "Upper Body Pull & Arms Density",
      warmup: "5 mins arm swings, jumping jacks, thoracic rotations",
      exercises: [
        { exercise: "Dumbbell Bent-Over Row", sets: 4, reps: "10", rest: "60 sec", notes: "Pull smoothly toward navel" },
        { exercise: "Bench / Chair Tricep Dips", sets: 3, reps: "12-15", rest: "60 sec", notes: "Maintain upright torso" },
        { exercise: "Dumbbell Bicep Curls", sets: 3, reps: "10-12", rest: "45 sec", notes: "Supinate wrists at top" },
        { exercise: "Standard Push-up", sets: 2, reps: "AMRAP", rest: "60 sec", notes: "Clean push-ups to technical failure" }
      ],
      cooldown: "5 mins tricep overhead stretches and seated bicep extensions",
      recoverySuggestion: "Electrolyte replenishment drink and balanced dinner.",
      completed: false
    },
    {
      day: "Friday",
      dayNumber: 5,
      focus: "Metabolic Conditioning & Core",
      warmup: "6 mins high knees, butt kicks, dynamic torso twists",
      exercises: [
        { exercise: "Mountain Climbers", sets: 3, reps: "40 sec", rest: "45 sec", notes: "Quick cadence with level pelvis" },
        { exercise: "Goblet Squat", sets: 3, reps: "15", rest: "60 sec", notes: "Faster tempo with good depth" },
        { exercise: "Plank Hold", sets: 3, reps: "45 sec", rest: "45 sec", notes: "Steady breathing" },
        { exercise: "Standard Push-up", sets: 3, reps: "10", rest: "45 sec", notes: "Explosive concentric phase" }
      ],
      cooldown: "6 mins full-body cool-down walk and hamstring stretch",
      recoverySuggestion: "Recharge with high-antioxidant smoothie (berries, spinach).",
      completed: false
    },
    {
      day: "Saturday",
      dayNumber: 6,
      focus: "Flexibility & Joint Decompression",
      warmup: "3 mins gentle neck and spine rolls",
      exercises: [
        { exercise: "World's Greatest Stretch", sets: 3, reps: "6 each side", rest: "30 sec", notes: "Open up hips and ankles" },
        { exercise: "Dead Hang from Pull-up Bar", sets: 3, reps: "30 sec", rest: "45 sec", notes: "Relax shoulders and decompress spine" }
      ],
      cooldown: "8 mins restorative yoga (cobra, pigeon pose)",
      recoverySuggestion: "Spend time outdoors in natural daylight.",
      completed: false
    },
    {
      day: "Sunday",
      dayNumber: 7,
      focus: "Full Rest & Mental Recharge",
      warmup: "None required",
      exercises: [
        { exercise: "Restorative Rest Day", sets: 1, reps: "All day", rest: "N/A", notes: "Allow tissue repair and glycogen replenishment" }
      ],
      cooldown: "Optional evening 15-min relaxing walk",
      recoverySuggestion: "Prep meals and review upcoming week's fitness goals.",
      completed: false
    }
  ]
};

export const initialNutrition: NutritionPlan = {
  dietaryPreference: "Vegetarian",
  estimatedCalories: 2250,
  proteinG: 135,
  carbsG: 260,
  fatsG: 65,
  meals: {
    breakfast: {
      name: "Oatmeal Power Bowl",
      description: "Rolled oats with chia seeds, scoop of plant protein, almond milk, banana slices, and chopped walnuts.",
      calories: 520,
      protein: "28g"
    },
    midMorning: {
      name: "Greek Yogurt & Berries",
      description: "Plain low-fat Greek yogurt topped with blueberries, pumpkin seeds, and a drizzle of raw honey.",
      calories: 220,
      protein: "16g"
    },
    lunch: {
      name: "Paneer/Tofu Quinoa Bowl",
      description: "Grilled spiced paneer or firm tofu, steamed broccoli, roasted chickpeas, quinoa, and spiced yellow dal.",
      calories: 680,
      protein: "38g"
    },
    eveningSnack: {
      name: "Roasted Makhana & Almonds",
      description: "Fox nuts lightly tossed in olive oil with 15 raw almonds and green tea.",
      calories: 210,
      protein: "8g"
    },
    dinner: {
      name: "Lentil Stew & Sautéed Greens",
      description: "Hearty red lentil curry with spinach, zucchini, carrots, and a small serving of brown basmati rice.",
      calories: 540,
      protein: "32g"
    }
  },
  preWorkout: "Banana and 1 tbsp peanut butter 45 minutes before training for fast-digesting glycogen.",
  postWorkout: "Protein shake with soy/whey isolate and a handful of dates within 45 minutes.",
  hydrationTip: "Drink 500ml water 1 hour prior to exercise and sip 150ml every 15-20 minutes during training."
};
