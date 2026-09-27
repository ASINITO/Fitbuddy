export interface UserProfile {
  id: number;
  fullName: string;
  username: string;
  email: string;
  isAdmin: boolean;
  age: number;
  gender: string;
  height: number; // cm
  weight: number; // kg
  fitnessGoal: string;
  fitnessLevel: 'Beginner' | 'Intermediate' | 'Advanced';
  preferredIntensity: 'Low' | 'Moderate' | 'High';
  preferredDuration: number; // minutes
  availableDays: number;
  equipment: string;
  dietaryPreference: string;
  preferredLanguage: string;
  createdAt: string;
}

export interface ExerciseDetail {
  exercise: string;
  sets: number;
  reps: string;
  rest: string;
  notes?: string;
}

export interface WorkoutDay {
  day: string;
  dayNumber: number;
  focus: string;
  warmup: string;
  exercises: ExerciseDetail[];
  cooldown: string;
  recoverySuggestion: string;
  completed: boolean;
}

export interface WorkoutPlan {
  id: number;
  title: string;
  goal: string;
  fitnessLevel: string;
  intensity: string;
  version: number;
  days: WorkoutDay[];
  createdAt: string;
}

export interface WorkoutHistoryItem {
  id: number;
  date: string;
  goal: string;
  intensity: string;
  focus: string;
  feedback?: string;
  completed: boolean;
}

export interface ExerciseItem {
  id: number;
  name: string;
  muscleGroup: 'Chest' | 'Back' | 'Legs' | 'Shoulders' | 'Arms' | 'Core' | 'Cardio' | 'Flexibility';
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  equipment: string;
  description: string;
  instructions: string[];
  safetyNotes: string;
}

export interface MealDetail {
  name: string;
  description: string;
  calories: number;
  protein: string;
}

export interface NutritionPlan {
  dietaryPreference: string;
  estimatedCalories: number;
  proteinG: number;
  carbsG: number;
  fatsG: number;
  meals: {
    breakfast: MealDetail;
    midMorning: MealDetail;
    lunch: MealDetail;
    eveningSnack: MealDetail;
    dinner: MealDetail;
  };
  preWorkout: string;
  postWorkout: string;
  hydrationTip: string;
}

export interface AchievementBadge {
  id: string;
  title: string;
  description: string;
  icon: string;
  category: string;
  points: number;
  unlocked: boolean;
  unlockedAt?: string;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'ai';
  message: string;
  language: string;
  timestamp: string;
}

export interface DailyCheckIn {
  id: string;
  date: string;
  energyLevel: number;
  mood: string;
  sleepQuality: string;
  muscleSoreness: string;
  stressLevel: number;
  workoutCompleted: boolean;
  waterIntakeMl: number;
  aiRecommendation?: string;
}

export interface BiometricLog {
  date: string;
  weight: number;
  steps: number;
  runningDistance: number;
}
