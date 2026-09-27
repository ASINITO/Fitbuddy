import React, { useState, useEffect } from 'react';
import {
  Activity,
  Dumbbell,
  Flame,
  Droplet,
  Moon,
  Sparkles,
  MessageSquare,
  Award,
  CheckCircle2,
  Circle,
  Play,
  RotateCcw,
  Sliders,
  ChevronRight,
  TrendingDown,
  Info,
  Shield,
  Search,
  User,
  AlertTriangle,
  Send,
  Plus,
  ArrowUpRight,
  X,
  Target
} from 'lucide-react';
import {
  UserProfile,
  WorkoutPlan,
  ExerciseItem,
  NutritionPlan,
  AchievementBadge,
  ChatMessage,
  DailyCheckIn
} from './types';
import {
  initialUser,
  initialPlan,
  initialExercises,
  initialBadges,
  initialNutrition
} from './mockData';

export default function App() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'workout' | 'exercises' | 'nutrition' | 'progress' | 'chat' | 'badges' | 'admin' | 'profile'>('dashboard');

  const [user, setUser] = useState<UserProfile>(() => {
    const saved = localStorage.getItem('fitbuddy_user');
    return saved ? JSON.parse(saved) : initialUser;
  });

  const [workoutPlan, setWorkoutPlan] = useState<WorkoutPlan>(() => {
    const saved = localStorage.getItem('fitbuddy_plan');
    return saved ? JSON.parse(saved) : initialPlan;
  });

  const [waterMl, setWaterMl] = useState<number>(() => {
    const saved = localStorage.getItem('fitbuddy_water');
    return saved ? JSON.parse(saved) : 1750;
  });

  const [badges, setBadges] = useState<AchievementBadge[]>(() => {
    const saved = localStorage.getItem('fitbuddy_badges');
    return saved ? JSON.parse(saved) : initialBadges;
  });

  const [nutrition, setNutrition] = useState<NutritionPlan>(() => {
    const saved = localStorage.getItem('fitbuddy_nutrition');
    return saved ? JSON.parse(saved) : initialNutrition;
  });

  const [chatMessages, setChatMessages] = useState<ChatMessage[]>(() => {
    const saved = localStorage.getItem('fitbuddy_chat');
    return saved ? JSON.parse(saved) : [
      {
        id: '1',
        sender: 'ai',
        message: 'Hello Alex! I am your FitBuddy AI Coach. I have your profile loaded (Muscle building & Wellness, Intermediate level). Ask me anything about your routine, exercise form, or recovery!',
        language: 'English',
        timestamp: 'Just now'
      }
    ];
  });

  const [checkIns, setCheckIns] = useState<DailyCheckIn[]>(() => {
    const saved = localStorage.getItem('fitbuddy_checkins');
    return saved ? JSON.parse(saved) : [
      {
        id: '1',
        date: 'Today',
        energyLevel: 4,
        mood: 'Energetic',
        sleepQuality: 'Good',
        muscleSoreness: 'Mild',
        stressLevel: 2,
        workoutCompleted: true,
        waterIntakeMl: 1750,
        aiRecommendation: 'Readiness markers look solid! Maintain good form on your programmed exercises, hit your hydration target, and finish with a 5-minute cooldown.'
      }
    ];
  });

  const [chatInput, setChatInput] = useState('');
  const [chatLanguage, setChatLanguage] = useState<'English' | 'Tamil'>('English');
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [adaptModalOpen, setAdaptModalOpen] = useState(false);
  const [adaptFeedback, setAdaptFeedback] = useState('');
  const [isAdapting, setIsAdapting] = useState(false);
  const [selectedExercise, setSelectedExercise] = useState<ExerciseItem | null>(null);
  const [exerciseGuide, setExerciseGuide] = useState<any>(null);
  const [isGuideLoading, setIsGuideLoading] = useState(false);
  const [exerciseFilter, setExerciseFilter] = useState('All');
  const [exerciseSearch, setExerciseSearch] = useState('');
  const [checkInModalOpen, setCheckInModalOpen] = useState(false);
  const [adminUserSearch, setAdminUserSearch] = useState('');
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  useEffect(() => { localStorage.setItem('fitbuddy_user', JSON.stringify(user)); }, [user]);
  useEffect(() => { localStorage.setItem('fitbuddy_plan', JSON.stringify(workoutPlan)); }, [workoutPlan]);
  useEffect(() => { localStorage.setItem('fitbuddy_water', JSON.stringify(waterMl)); }, [waterMl]);
  useEffect(() => { localStorage.setItem('fitbuddy_badges', JSON.stringify(badges)); }, [badges]);
  useEffect(() => { localStorage.setItem('fitbuddy_nutrition', JSON.stringify(nutrition)); }, [nutrition]);
  useEffect(() => { localStorage.setItem('fitbuddy_chat', JSON.stringify(chatMessages)); }, [chatMessages]);
  useEffect(() => { localStorage.setItem('fitbuddy_checkins', JSON.stringify(checkIns)); }, [checkIns]);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3500);
  };

  const heightM = user.height / 100;
  const bmiValue = (user.weight / (heightM * heightM)).toFixed(1);
  const getBmiCategory = (bmi: number) => {
    if (bmi < 18.5) return { label: 'Underweight', color: 'text-amber-400' };
    if (bmi < 25) return { label: 'Normal weight', color: 'text-emerald-400' };
    if (bmi < 30) return { label: 'Overweight', color: 'text-amber-400' };
    return { label: 'Obese', color: 'text-rose-400' };
  };
  const bmiCategory = getBmiCategory(parseFloat(bmiValue));

  const bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age + 5;
  const maintenanceCalories = Math.round(bmr * 1.55);

  const completedCount = workoutPlan.days.filter(d => d.completed).length;
  const weeklyCompletionRate = Math.round((completedCount / user.availableDays) * 100);

  const handleToggleDay = (dayNumber: number) => {
    const updatedDays = workoutPlan.days.map(d => {
      if (d.dayNumber === dayNumber) {
        return { ...d, completed: !d.completed };
      }
      return d;
    });

    setWorkoutPlan({
      ...workoutPlan,
      days: updatedDays
    });

    const anyDone = updatedDays.some(d => d.completed);
    if (anyDone) {
      setBadges(prev => prev.map(b => b.id === 'first_workout' ? { ...b, unlocked: true, unlockedAt: 'Today' } : b));
    }
    showToast(`Day ${dayNumber} status updated!`);
  };

  const handleAddWater = (amt: number) => {
    const nextVal = waterMl + amt;
    setWaterMl(nextVal);
    if (nextVal >= 2500) {
      setBadges(prev => prev.map(b => b.id === 'hydration_hero' ? { ...b, unlocked: true, unlockedAt: 'Today' } : b));
    }
    showToast(`Added ${amt}ml of water! Total: ${nextVal}ml`);
  };

  const handleAdaptPlan = async () => {
    if (!adaptFeedback.trim()) return;
    setIsAdapting(true);
    try {
      const res = await fetch('/api/gemini/adapt-workout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          currentPlan: workoutPlan.days,
          feedback: adaptFeedback,
          profile: user
        })
      });
      const data = await res.json();
      if (data.success && Array.isArray(data.plan)) {
        setWorkoutPlan({
          ...workoutPlan,
          days: data.plan,
          version: workoutPlan.version + 1
        });
        showToast(`AI adapted plan to: "${adaptFeedback}"`);
      } else {
        const adaptedDays = workoutPlan.days.map(d => {
          if (adaptFeedback.toLowerCase().includes('easier')) {
            return {
              ...d,
              recoverySuggestion: `${d.recoverySuggestion} (Adapted: Reduced volume for gentler stimulus).`,
              exercises: d.exercises.map(ex => ({ ...ex, sets: Math.max(2, ex.sets - 1), rest: '90 sec' }))
            };
          }
          if (adaptFeedback.toLowerCase().includes('30')) {
            return {
              ...d,
              warmup: '3 mins quick mobility',
              cooldown: '2 mins stretch',
              exercises: d.exercises.slice(0, 3)
            };
          }
          return d;
        });
        setWorkoutPlan({
          ...workoutPlan,
          days: adaptedDays,
          version: workoutPlan.version + 1
        });
        showToast('Plan adapted with custom modifications!');
      }
      setAdaptModalOpen(false);
      setAdaptFeedback('');
    } catch (e) {
      showToast('Adaptation applied with local optimization.');
      setAdaptModalOpen(false);
    } finally {
      setIsAdapting(false);
    }
  };

  const handleOpenExerciseGuide = async (exercise: ExerciseItem) => {
    setSelectedExercise(exercise);
    setIsGuideLoading(true);
    setExerciseGuide(null);
    try {
      const res = await fetch('/api/gemini/explain-exercise', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ exerciseName: exercise.name })
      });
      const json = await res.json();
      if (json.data) {
        setExerciseGuide(json.data);
      }
    } catch (e) {
      setExerciseGuide({
        purpose: exercise.description,
        instructions: exercise.instructions,
        commonMistakes: ['Rushing through reps', 'Improper joint alignment', 'Holding breath'],
        beginnerModification: 'Perform using bodyweight or reduced load.',
        safetyNotes: exercise.safetyNotes
      });
    } finally {
      setIsGuideLoading(false);
    }
  };

  const handleSendChat = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!chatInput.trim() || isChatLoading) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      message: chatInput.trim(),
      language: chatLanguage,
      timestamp: 'Just now'
    };

    setChatMessages(prev => [...prev, userMsg]);
    const promptText = chatInput.trim();
    setChatInput('');
    setIsChatLoading(true);

    try {
      const res = await fetch('/api/gemini/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: promptText,
          language: chatLanguage,
          userProfile: user
        })
      });
      const data = await res.json();
      const aiReply: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        message: data.reply || "I'm here to support your fitness journey. What would you like to review?",
        language: chatLanguage,
        timestamp: 'Just now'
      };
      setChatMessages(prev => [...prev, aiReply]);
    } catch (err) {
      const fallbackReply: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        message: chatLanguage === 'Tamil'
          ? 'வணக்கம்! உடற்பயிற்சிக்கு முன் போதுமான அளவு தண்ணீர் குடியுங்கள். உங்கள் ஆரோக்கிய இலக்கை அடைய தொடர்ந்து பயிற்சி செய்யுங்கள்.'
          : `Great question, ${user.fullName}. Focus on strict form, adequate protein intake, and consistent sleep. Let me know if you need specific exercise variations!`,
        language: chatLanguage,
        timestamp: 'Just now'
      };
      setChatMessages(prev => [...prev, fallbackReply]);
    } finally {
      setIsChatLoading(false);
    }
  };

  const handleCheckInSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const energy = Number(formData.get('energy')) || 4;
    const mood = formData.get('mood') as string || 'Good';
    const soreness = formData.get('soreness') as string || 'None';
    const sleep = formData.get('sleep') as string || 'Good';

    let rec = 'Stay focused on consistent progressive overload and hit your 2.5L water target today.';
    try {
      const res = await fetch('/api/gemini/daily-recommendation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          checkIn: { energyLevel: energy, mood, muscleSoreness: soreness, sleepQuality: sleep },
          userProfile: user
        })
      });
      const data = await res.json();
      if (data.recommendation) rec = data.recommendation;
    } catch (err) {}

    const newCheckIn: DailyCheckIn = {
      id: Date.now().toString(),
      date: 'Today',
      energyLevel: energy,
      mood,
      sleepQuality: sleep,
      muscleSoreness: soreness,
      stressLevel: 2,
      workoutCompleted: workoutPlan.days[0].completed,
      waterIntakeMl: waterMl,
      aiRecommendation: rec
    };

    setCheckIns([newCheckIn, ...checkIns]);
    setCheckInModalOpen(false);
    showToast('Check-in saved! AI recommendation updated.');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-emerald-500 selection:text-slate-950">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-emerald-500 text-slate-950 font-bold px-4 py-2.5 rounded-xl shadow-2xl text-xs flex items-center gap-2 border border-emerald-400">
          <Sparkles className="w-4 h-4" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Global Medical Disclaimer Header Bar */}
      <aside className="bg-amber-950/40 border-b border-amber-900/40 px-4 py-1.5 text-center text-[11px] text-amber-300 flex items-center justify-center gap-2">
        <AlertTriangle className="w-3.5 h-3.5 flex-shrink-0 text-amber-400" />
        <span>
          <strong>General Wellness Notice:</strong> FitBuddy AI provides automated general fitness suggestions and does not substitute professional medical diagnosis or personalized physical therapy. Consult a physician before starting any rigorous workout.
        </span>
      </aside>

      {/* Primary Navigation Bar */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-500 to-cyan-500 flex items-center justify-center text-slate-950 font-black shadow-lg shadow-emerald-500/20">
              FB
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                FitBuddy
              </span>
              <span className="hidden sm:inline-block ml-2 text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Gemini 3.8 Flash
              </span>
            </div>
          </div>

          {/* Desktop Nav Tabs */}
          <nav className="hidden lg:flex items-center space-x-1 text-xs font-semibold">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: Activity },
              { id: 'workout', label: 'Workouts', icon: Dumbbell },
              { id: 'exercises', label: 'Exercise Library', icon: Info },
              { id: 'nutrition', label: 'Nutrition', icon: Flame },
              { id: 'progress', label: 'Progress & Charts', icon: TrendingDown },
              { id: 'chat', label: 'AI Coach', icon: MessageSquare },
              { id: 'badges', label: 'Milestones', icon: Award },
              { id: 'admin', label: 'Admin Hub', icon: Shield },
              { id: 'profile', label: 'Settings', icon: User }
            ].map(tab => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`px-3 py-2 rounded-lg flex items-center gap-1.5 transition ${
                    isActive
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  {tab.label}
                </button>
              );
            })}
          </nav>

          <div className="flex items-center space-x-3">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60 text-xs">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="font-medium text-slate-300">{user.fullName}</span>
            </div>
            <button
              onClick={() => setActiveTab('profile')}
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
              title="Profile Settings"
            >
              <User className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Mobile Navigation Scrollbar */}
        <div className="lg:hidden flex items-center overflow-x-auto px-4 py-2 border-t border-slate-800/60 gap-1 text-xs">
          {[
            { id: 'dashboard', label: 'Dashboard' },
            { id: 'workout', label: 'Workout' },
            { id: 'exercises', label: 'Library' },
            { id: 'nutrition', label: 'Nutrition' },
            { id: 'progress', label: 'Progress' },
            { id: 'chat', label: 'AI Coach' },
            { id: 'badges', label: 'Badges' },
            { id: 'admin', label: 'Admin' },
            { id: 'profile', label: 'Profile' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-3 py-1.5 rounded-lg whitespace-nowrap font-medium text-xs ${
                activeTab === tab.id ? 'bg-emerald-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        {/* 1. DASHBOARD */}
        {activeTab === 'dashboard' && (
          <div className="space-y-8">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
              <div>
                <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center gap-2">
                  Welcome back, <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">{user.fullName}</span>!
                </h1>
                <p className="text-xs sm:text-sm text-slate-400 mt-1 flex flex-wrap items-center gap-2">
                  <span>Goal: <strong className="text-slate-200">{user.fitnessGoal}</strong></span>
                  <span>•</span>
                  <span>Level: <strong className="text-slate-200">{user.fitnessLevel}</strong></span>
                  <span>•</span>
                  <span>Target: <strong className="text-slate-200">{user.availableDays} Days/Week</strong></span>
                </p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => setActiveTab('workout')}
                  className="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold rounded-xl text-xs flex items-center gap-1.5 shadow-md shadow-emerald-500/20 transition"
                >
                  <Play className="w-4 h-4 fill-slate-950" /> Today's Workout
                </button>
                <button
                  onClick={() => setActiveTab('chat')}
                  className="px-3.5 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 font-semibold rounded-xl text-xs flex items-center gap-1.5 transition"
                >
                  <Sparkles className="w-4 h-4 text-cyan-400" /> Ask AI
                </button>
              </div>
            </div>

            {/* Metric Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 relative overflow-hidden">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">BMI Index</span>
                  <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-400"><Activity className="w-4 h-4" /></div>
                </div>
                <div className="mt-4 flex items-baseline gap-2">
                  <span className="text-3xl font-black text-white">{bmiValue}</span>
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full bg-slate-800 ${bmiCategory.color}`}>
                    {bmiCategory.label}
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 mt-2">Screening metric • Weight: {user.weight}kg</p>
              </div>

              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 relative overflow-hidden">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Est. Calories</span>
                  <div className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400"><Flame className="w-4 h-4" /></div>
                </div>
                <div className="mt-4 flex items-baseline gap-2">
                  <span className="text-3xl font-black text-white">{maintenanceCalories}</span>
                  <span className="text-xs text-slate-400">kcal/day</span>
                </div>
                <p className="text-[11px] text-slate-500 mt-2">Mifflin-St Jeor formula estimate</p>
              </div>

              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 relative overflow-hidden">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Workout Streak</span>
                  <div className="p-2 rounded-xl bg-amber-500/10 text-amber-400"><Sparkles className="w-4 h-4" /></div>
                </div>
                <div className="mt-4 flex items-baseline gap-2">
                  <span className="text-3xl font-black text-white">4</span>
                  <span className="text-xs text-amber-400 font-semibold">Days active 🔥</span>
                </div>
                <p className="text-[11px] text-slate-500 mt-2">Best: 7 consecutive days</p>
              </div>

              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 relative overflow-hidden">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Weekly Progress</span>
                  <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-400"><Target className="w-4 h-4" /></div>
                </div>
                <div className="mt-4 flex items-baseline gap-2">
                  <span className="text-3xl font-black text-white">{weeklyCompletionRate}%</span>
                  <span className="text-xs text-slate-400">{completedCount} / {user.availableDays} workouts</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
                  <div className="bg-emerald-500 h-full rounded-full transition-all duration-500" style={{ width: `${Math.min(100, weeklyCompletionRate)}%` }}></div>
                </div>
              </div>
            </div>

            {/* Layout: Today's Workout + Trackers */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 space-y-6">
                <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-sm">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-800">
                    <div>
                      <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">Day 1 Scheduled Routine</span>
                      <h2 className="text-lg sm:text-xl font-bold text-white mt-0.5">{workoutPlan.days[0].focus}</h2>
                    </div>
                    <button
                      onClick={() => handleToggleDay(1)}
                      className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 ${
                        workoutPlan.days[0].completed
                          ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20'
                          : 'bg-slate-800 text-slate-300 hover:bg-emerald-500 hover:text-slate-950'
                      }`}
                    >
                      {workoutPlan.days[0].completed ? <CheckCircle2 className="w-4 h-4" /> : <Circle className="w-4 h-4" />}
                      {workoutPlan.days[0].completed ? 'Workout Completed' : 'Mark as Done'}
                    </button>
                  </div>

                  <div className="mt-4 space-y-3">
                    {workoutPlan.days[0].exercises.map((ex, idx) => (
                      <div key={idx} className="flex flex-col sm:flex-row sm:items-center justify-between p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 gap-2">
                        <div>
                          <strong className="text-sm font-semibold text-white">{ex.exercise}</strong>
                          <p className="text-[11px] text-slate-400 mt-0.5">{ex.notes || 'Control tempo and maintain proper form.'}</p>
                        </div>
                        <div className="text-right text-xs font-mono text-emerald-400 font-bold">
                          {ex.sets} sets × {ex.reps}
                          <div className="text-[10px] text-slate-500 font-sans">Rest: {ex.rest}</div>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="mt-6 pt-4 border-t border-slate-800/80 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                    <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
                      <strong className="text-cyan-400 block mb-1">Warm-up Protocol:</strong>
                      <span className="text-slate-300">{workoutPlan.days[0].warmup}</span>
                    </div>
                    <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
                      <strong className="text-emerald-400 block mb-1">Recovery Suggestion:</strong>
                      <span className="text-slate-300">{workoutPlan.days[0].recoverySuggestion}</span>
                    </div>
                  </div>
                </div>

                <div className="p-5 rounded-2xl bg-gradient-to-r from-emerald-950/40 to-cyan-950/30 border border-emerald-500/20 flex items-start gap-4">
                  <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 flex-shrink-0">
                    <Sparkles className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white flex items-center gap-2">
                      AI Wellness & Readiness Advisory
                      <span className="text-[10px] uppercase font-bold text-emerald-400 px-2 py-0.5 bg-emerald-500/10 rounded-full">
                        Gemini 3.8 Flash
                      </span>
                    </h3>
                    <p className="text-xs text-slate-300 mt-1.5 leading-relaxed">
                      {checkIns[0]?.aiRecommendation || 'Consistent effort on your compound exercises today! Ensure 500ml water before sleep to accelerate glycogen recovery.'}
                    </p>
                  </div>
                </div>
              </div>

              {/* Right Column: Trackers */}
              <div className="space-y-6">
                <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Droplet className="w-5 h-5 text-cyan-400" />
                      <h3 className="text-sm font-bold text-white">Hydration Tracker</h3>
                    </div>
                    <span className="text-xs font-bold text-cyan-400">{Math.min(100, Math.round((waterMl / 2500) * 100))}%</span>
                  </div>

                  <div className="flex items-baseline justify-between mb-2">
                    <span className="text-2xl font-black text-white">{waterMl} ml</span>
                    <span className="text-xs text-slate-400">Target: 2500 ml</span>
                  </div>

                  <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden mb-4">
                    <div
                      className="bg-cyan-400 h-full rounded-full transition-all duration-300"
                      style={{ width: `${Math.min(100, (waterMl / 2500) * 100)}%` }}
                    ></div>
                  </div>

                  <div className="grid grid-cols-2 gap-2">
                    <button
                      onClick={() => handleAddWater(250)}
                      className="py-2.5 px-3 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-xl border border-slate-700 transition"
                    >
                      + 1 Glass (250ml)
                    </button>
                    <button
                      onClick={() => handleAddWater(500)}
                      className="py-2.5 px-3 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-xl border border-slate-700 transition"
                    >
                      + Bottle (500ml)
                    </button>
                  </div>
                </div>

                <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Moon className="w-5 h-5 text-indigo-400" />
                      <h3 className="text-sm font-bold text-white">Sleep Recovery</h3>
                    </div>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-indigo-300 font-semibold">Optimal</span>
                  </div>

                  <div className="flex items-baseline justify-between mb-4">
                    <span className="text-2xl font-black text-white">7.8 hrs</span>
                    <span className="text-xs text-slate-400">Range: 7–9 hrs</span>
                  </div>

                  <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/80 text-xs text-slate-300 leading-relaxed">
                    <span className="text-indigo-400 font-semibold block mb-0.5">Recovery Insight:</span>
                    Quality REM and deep sleep support muscle protein synthesis and nervous system reset.
                  </div>
                </div>

                <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 text-center">
                  <Activity className="w-7 h-7 text-emerald-400 mx-auto mb-2" />
                  <h3 className="text-sm font-bold text-white">Daily Wellness Check-In</h3>
                  <p className="text-xs text-slate-400 mt-1 mb-4 leading-relaxed">
                    Rate energy, soreness, and mood to tune your next AI workout adaptation.
                  </p>
                  <button
                    onClick={() => setCheckInModalOpen(true)}
                    className="w-full py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold rounded-xl text-xs border border-slate-700 transition"
                  >
                    Submit Readiness Log
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 2. WORKOUT TAB */}
        {activeTab === 'workout' && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-2xl sm:text-3xl font-black text-white">{workoutPlan.title}</h1>
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    v{workoutPlan.version}.0
                  </span>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Goal: {workoutPlan.goal} • Level: {workoutPlan.fitnessLevel} • Intensity: {workoutPlan.intensity}
                </p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => setAdaptModalOpen(true)}
                  className="px-4 py-2 bg-gradient-to-r from-emerald-500 to-cyan-500 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-emerald-500/20 hover:opacity-95 transition flex items-center gap-1.5"
                >
                  <Sliders className="w-4 h-4" /> Adapt Plan with AI
                </button>
              </div>
            </div>

            <div className="space-y-4">
              {workoutPlan.days.map(day => (
                <div key={day.dayNumber} className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden transition">
                  <div className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-900/80">
                    <div className="flex items-center gap-3">
                      <span className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 font-bold flex items-center justify-center text-xs">
                        {day.dayNumber}
                      </span>
                      <div>
                        <h3 className="text-sm font-bold text-white">
                          {day.day}: <span className="text-emerald-400">{day.focus}</span>
                        </h3>
                        <p className="text-[11px] text-slate-400 mt-0.5">Warm-up: {day.warmup}</p>
                      </div>
                    </div>

                    <button
                      onClick={() => handleToggleDay(day.dayNumber)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                        day.completed
                          ? 'bg-emerald-500 text-slate-950 font-bold'
                          : 'bg-slate-800 text-slate-300 hover:bg-emerald-500 hover:text-slate-950'
                      }`}
                    >
                      {day.completed ? <CheckCircle2 className="w-3.5 h-3.5" /> : <Circle className="w-3.5 h-3.5" />}
                      {day.completed ? 'Completed' : 'Mark Done'}
                    </button>
                  </div>

                  <div className="px-5 py-4 border-t border-slate-800/80 space-y-2.5">
                    {day.exercises.map((ex, i) => (
                      <div key={i} className="flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 gap-2">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-semibold text-white">{ex.exercise}</span>
                          <span className="text-[11px] text-slate-400">• {ex.notes || 'Full range of motion'}</span>
                        </div>
                        <div className="flex items-center gap-4 text-xs font-mono text-emerald-400 font-bold">
                          <span>{ex.sets} sets × {ex.reps}</span>
                          <span className="text-slate-500 text-[10px] font-sans">Rest: {ex.rest}</span>
                        </div>
                      </div>
                    ))}

                    <div className="pt-2 flex flex-col sm:flex-row gap-3 text-[11px] text-slate-400">
                      <div className="flex-1 p-2.5 rounded-lg bg-slate-950/40 border border-slate-800/60">
                        <strong className="text-cyan-400">Cooldown:</strong> {day.cooldown}
                      </div>
                      <div className="flex-1 p-2.5 rounded-lg bg-slate-950/40 border border-slate-800/60">
                        <strong className="text-emerald-400">Recovery Suggestion:</strong> {day.recoverySuggestion}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 3. EXERCISE LIBRARY TAB */}
        {activeTab === 'exercises' && (
          <div className="space-y-6">
            <div className="pb-4 border-b border-slate-800">
              <h1 className="text-2xl sm:text-3xl font-black text-white">Exercise Database & AI Form Coach</h1>
              <p className="text-xs text-slate-400 mt-1">
                Explore biomechanical instructions, safety guidelines, and ask Gemini AI for individualized movement regressions.
              </p>
            </div>

            <div className="p-4 bg-slate-900 border border-slate-800 rounded-2xl flex flex-col sm:flex-row gap-4">
              <div className="relative flex-1">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                <input
                  type="text"
                  placeholder="Search exercise by name..."
                  value={exerciseSearch}
                  onChange={e => setExerciseSearch(e.target.value)}
                  className="w-full pl-9 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
              <div className="flex items-center gap-2 overflow-x-auto text-xs">
                {['All', 'Chest', 'Back', 'Legs', 'Shoulders', 'Arms', 'Core', 'Cardio', 'Flexibility'].map(mg => (
                  <button
                    key={mg}
                    onClick={() => setExerciseFilter(mg)}
                    className={`px-3 py-1.5 rounded-lg whitespace-nowrap font-medium transition ${
                      exerciseFilter === mg
                        ? 'bg-emerald-500 text-slate-950 font-bold'
                        : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
                    }`}
                  >
                    {mg}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {initialExercises
                .filter(ex => {
                  const matchSearch = ex.name.toLowerCase().includes(exerciseSearch.toLowerCase());
                  const matchGroup = exerciseFilter === 'All' || ex.muscleGroup === exerciseFilter;
                  return matchSearch && matchGroup;
                })
                .map(exercise => (
                  <div key={exercise.id} className="p-5 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col justify-between hover:border-emerald-500/40 transition">
                    <div>
                      <div className="flex items-center justify-between">
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                          {exercise.muscleGroup}
                        </span>
                        <span className="text-[10px] text-slate-500 font-mono">{exercise.difficulty}</span>
                      </div>
                      <h3 className="text-base font-bold text-white mt-2">{exercise.name}</h3>
                      <p className="text-xs text-slate-400 mt-1 leading-relaxed">{exercise.description}</p>
                      <div className="mt-3 text-[11px] text-slate-500 font-mono">
                        Equipment: <strong className="text-slate-300 font-sans">{exercise.equipment}</strong>
                      </div>
                    </div>

                    <button
                      onClick={() => handleOpenExerciseGuide(exercise)}
                      className="mt-5 w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 transition flex items-center justify-center gap-1.5"
                    >
                      <Sparkles className="w-3.5 h-3.5 text-cyan-400" /> Ask AI to Explain Form
                    </button>
                  </div>
                ))}
            </div>
          </div>
        )}

        {/* 4. NUTRITION TAB */}
        {activeTab === 'nutrition' && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
              <div>
                <h1 className="text-2xl sm:text-3xl font-black text-white">AI Nutrition & Meal Guidance</h1>
                <p className="text-xs text-slate-400 mt-1">
                  Balanced meal structures for {nutrition.dietaryPreference} diet supporting muscle synthesis and recovery.
                </p>
              </div>
              <button
                onClick={() => showToast('Refreshed nutritional macro targets!')}
                className="px-4 py-2 bg-gradient-to-r from-emerald-500 to-cyan-500 text-slate-950 font-bold text-xs rounded-xl shadow-md transition"
              >
                Recalculate Macros
              </button>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Target Calories</span>
                <div className="text-2xl font-black text-white mt-1">{nutrition.estimatedCalories} kcal</div>
              </div>
              <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
                <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">Protein Target</span>
                <div className="text-2xl font-black text-emerald-400 mt-1">{nutrition.proteinG} g</div>
              </div>
              <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
                <span className="text-[10px] font-bold text-cyan-400 uppercase tracking-wider">Carbohydrates</span>
                <div className="text-2xl font-black text-cyan-400 mt-1">{nutrition.carbsG} g</div>
              </div>
              <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
                <span className="text-[10px] font-bold text-amber-400 uppercase tracking-wider">Healthy Fats</span>
                <div className="text-2xl font-black text-amber-400 mt-1">{nutrition.fatsG} g</div>
              </div>
            </div>

            <div className="space-y-3">
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">Daily Meal Structure</h2>
              <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                {[
                  { key: 'breakfast', label: 'Breakfast', data: nutrition.meals.breakfast },
                  { key: 'midMorning', label: 'Mid-Morning', data: nutrition.meals.midMorning },
                  { key: 'lunch', label: 'Lunch', data: nutrition.meals.lunch },
                  { key: 'eveningSnack', label: 'Evening Snack', data: nutrition.meals.eveningSnack },
                  { key: 'dinner', label: 'Dinner', data: nutrition.meals.dinner }
                ].map(meal => (
                  <div key={meal.key} className="p-4 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col justify-between">
                    <div>
                      <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">{meal.label}</span>
                      <h4 className="text-xs font-bold text-white mt-1">{meal.data.name}</h4>
                      <p className="text-[11px] text-slate-400 mt-2 leading-relaxed">{meal.data.description}</p>
                    </div>
                    <div className="mt-4 pt-3 border-t border-slate-800 text-[10px] text-slate-400 flex justify-between font-mono">
                      <span>{meal.data.calories} kcal</span>
                      <span className="text-emerald-400 font-bold">{meal.data.protein}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4 border-t border-slate-800">
              <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800">
                <h3 className="text-xs font-bold text-cyan-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <Flame className="w-4 h-4" /> Pre-Workout Fuel
                </h3>
                <p className="text-xs text-slate-300 leading-relaxed">{nutrition.preWorkout}</p>
              </div>
              <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800">
                <h3 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4" /> Post-Workout Recovery
                </h3>
                <p className="text-xs text-slate-300 leading-relaxed">{nutrition.postWorkout}</p>
              </div>
              <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800">
                <h3 className="text-xs font-bold text-blue-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <Droplet className="w-4 h-4" /> Hydration Guideline
                </h3>
                <p className="text-xs text-slate-300 leading-relaxed">{nutrition.hydrationTip}</p>
              </div>
            </div>
          </div>
        )}

        {/* 5. PROGRESS & CHARTS TAB */}
        {activeTab === 'progress' && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
              <div>
                <h1 className="text-2xl sm:text-3xl font-black text-white">Progress Analytics & Biometrics</h1>
                <p className="text-xs text-slate-400 mt-1">Review weight trajectory, activity completion, and recovery consistency</p>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <TrendingDown className="w-4 h-4 text-emerald-400" /> Body Weight Progression (kg)
                  </h3>
                  <span className="text-xs text-emerald-400 font-bold">-2.3 kg total</span>
                </div>
                <div className="h-52 flex items-end justify-between pt-8 pb-2 px-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
                  {[
                    { date: 'Sep 1', val: 78.8 },
                    { date: 'Sep 6', val: 78.2 },
                    { date: 'Sep 11', val: 77.9 },
                    { date: 'Sep 16', val: 77.4 },
                    { date: 'Sep 21', val: 76.9 },
                    { date: 'Today', val: 76.5 }
                  ].map((pt, idx) => {
                    const heightPct = Math.round(((pt.val - 75) / 5) * 100);
                    return (
                      <div key={idx} className="flex flex-col items-center gap-2 flex-1">
                        <span className="text-[10px] font-mono text-emerald-400 font-semibold">{pt.val}</span>
                        <div className="w-8 bg-emerald-500/20 border-t-2 border-emerald-400 rounded-t-md transition-all" style={{ height: `${heightPct}%` }}></div>
                        <span className="text-[10px] text-slate-500 font-mono">{pt.date}</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <Activity className="w-4 h-4 text-cyan-400" /> Weekly Activity & Steps
                  </h3>
                  <span className="text-xs text-cyan-400 font-bold">Avg 9,200 steps/day</span>
                </div>
                <div className="h-52 flex items-end justify-between pt-8 pb-2 px-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
                  {[
                    { day: 'Mon', steps: 8500 },
                    { day: 'Tue', steps: 10400 },
                    { day: 'Wed', steps: 7200 },
                    { day: 'Thu', steps: 9800 },
                    { day: 'Fri', steps: 11200 },
                    { day: 'Sat', steps: 8900 },
                    { day: 'Sun', steps: 9400 }
                  ].map((d, i) => {
                    const pct = Math.round((d.steps / 12000) * 100);
                    return (
                      <div key={i} className="flex flex-col items-center gap-2 flex-1">
                        <span className="text-[10px] font-mono text-cyan-400 font-semibold">{d.steps}</span>
                        <div className="w-8 bg-cyan-500/30 border-t-2 border-cyan-400 rounded-t-md transition-all" style={{ height: `${pct}%` }}></div>
                        <span className="text-[10px] text-slate-500 font-mono">{d.day}</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <Droplet className="w-4 h-4 text-blue-400" /> Hydration Trends (ml)
                  </h3>
                  <span className="text-xs text-blue-400 font-bold">Goal: 2500 ml</span>
                </div>
                <div className="h-52 flex items-end justify-between pt-8 pb-2 px-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
                  {[
                    { day: 'Mon', ml: 2250 },
                    { day: 'Tue', ml: 2500 },
                    { day: 'Wed', ml: 2000 },
                    { day: 'Thu', ml: 2750 },
                    { day: 'Fri', ml: 2500 },
                    { day: 'Sat', ml: 2250 },
                    { day: 'Today', ml: waterMl }
                  ].map((w, i) => {
                    const pct = Math.round((w.ml / 3000) * 100);
                    return (
                      <div key={i} className="flex flex-col items-center gap-2 flex-1">
                        <span className="text-[10px] font-mono text-blue-400 font-semibold">{w.ml}</span>
                        <div className="w-8 bg-blue-500/30 border-t-2 border-blue-400 rounded-t-md transition-all" style={{ height: `${pct}%` }}></div>
                        <span className="text-[10px] text-slate-500 font-mono">{w.day}</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <Moon className="w-4 h-4 text-indigo-400" /> Sleep Duration (Hours)
                  </h3>
                  <span className="text-xs text-indigo-400 font-bold">7.7 hrs average</span>
                </div>
                <div className="h-52 flex items-end justify-between pt-8 pb-2 px-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
                  {[
                    { day: 'Mon', hrs: 7.2 },
                    { day: 'Tue', hrs: 7.8 },
                    { day: 'Wed', hrs: 6.9 },
                    { day: 'Thu', hrs: 8.1 },
                    { day: 'Fri', hrs: 7.5 },
                    { day: 'Sat', hrs: 8.5 },
                    { day: 'Sun', hrs: 7.8 }
                  ].map((s, i) => {
                    const pct = Math.round((s.hrs / 10) * 100);
                    return (
                      <div key={i} className="flex flex-col items-center gap-2 flex-1">
                        <span className="text-[10px] font-mono text-indigo-400 font-semibold">{s.hrs}h</span>
                        <div className="w-8 bg-indigo-500/30 border-t-2 border-indigo-400 rounded-t-md transition-all" style={{ height: `${pct}%` }}></div>
                        <span className="text-[10px] text-slate-500 font-mono">{s.day}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 6. CHATBOT TAB */}
        {activeTab === 'chat' && (
          <div className="max-w-4xl mx-auto h-[calc(100vh-12rem)] flex flex-col">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800 flex-shrink-0">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-cyan-500 flex items-center justify-center text-slate-950 font-black shadow-lg shadow-emerald-500/20">
                  <Sparkles className="w-5 h-5" />
                </div>
                <div>
                  <h1 className="text-base font-bold text-white flex items-center gap-2">
                    FitBuddy AI Coach
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  </h1>
                  <p className="text-xs text-slate-400">Context-aware fitness and recovery assistant</p>
                </div>
              </div>

              <div className="flex items-center gap-2 text-xs">
                <span className="text-slate-400">Language:</span>
                <select
                  value={chatLanguage}
                  onChange={e => setChatLanguage(e.target.value as any)}
                  className="bg-slate-900 border border-slate-700 text-white rounded-lg px-2.5 py-1 text-xs focus:outline-none focus:border-emerald-500"
                >
                  <option value="English">English</option>
                  <option value="Tamil">தமிழ் (Tamil)</option>
                </select>
              </div>
            </div>

            <div className="flex items-center gap-2 overflow-x-auto py-3 flex-shrink-0 text-xs no-scrollbar">
              {[
                'What workout should I do today?',
                'How can I improve my recovery?',
                'Explain squats.',
                'Give me a 5-minute warm-up.',
                'Suggest a healthy post-workout meal.'
              ].map((chip, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setChatInput(chip);
                  }}
                  className="px-3 py-1.5 rounded-full bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 whitespace-nowrap text-[11px]"
                >
                  {chip}
                </button>
              ))}
            </div>

            <div className="flex-1 overflow-y-auto space-y-4 py-4 pr-2">
              {chatMessages.map(msg => (
                <div
                  key={msg.id}
                  className={`flex items-start gap-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  {msg.sender === 'ai' && (
                    <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center flex-shrink-0 text-xs font-bold">
                      FB
                    </div>
                  )}
                  <div
                    className={`p-3.5 rounded-2xl text-xs leading-relaxed max-w-xl whitespace-pre-wrap ${
                      msg.sender === 'user'
                        ? 'bg-emerald-500 text-slate-950 font-medium'
                        : 'bg-slate-900 border border-slate-800 text-slate-200'
                    }`}
                  >
                    {msg.message}
                  </div>
                </div>
              ))}
              {isChatLoading && (
                <div className="flex items-center gap-2 text-xs text-slate-400 p-3">
                  <div className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></div>
                  <span>FitBuddy is thinking...</span>
                </div>
              )}
            </div>

            <form onSubmit={handleSendChat} className="pt-3 border-t border-slate-800 flex items-center gap-2 flex-shrink-0">
              <input
                type="text"
                placeholder={chatLanguage === 'Tamil' ? 'உடற்பயிற்சி அல்லது உணவு பற்றி கேளுங்கள்...' : 'Ask about workouts, form, nutrition, or recovery...'}
                value={chatInput}
                onChange={e => setChatInput(e.target.value)}
                className="flex-1 px-4 py-3 bg-slate-900 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-emerald-500 transition"
              />
              <button
                type="submit"
                disabled={isChatLoading}
                className="px-5 py-3 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-slate-950 font-bold rounded-xl text-xs transition shadow-md shadow-emerald-500/20"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        )}

        {/* 7. BADGES TAB */}
        {activeTab === 'badges' && (
          <div className="space-y-6">
            <div className="pb-4 border-b border-slate-800">
              <h1 className="text-2xl sm:text-3xl font-black text-white">Achievements & Badges</h1>
              <p className="text-xs text-slate-400 mt-1">
                Gamified milestone system rewarding consistency, hydration discipline, and workout completion.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {badges.map(b => (
                <div
                  key={b.id}
                  className={`p-6 rounded-2xl border transition ${
                    b.unlocked
                      ? 'bg-slate-900 border-emerald-500/40 shadow-lg shadow-emerald-500/5'
                      : 'bg-slate-900/50 border-slate-800/80 opacity-60'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-lg ${
                      b.unlocked ? 'bg-emerald-500/10 text-emerald-400' : 'bg-slate-800 text-slate-500'
                    }`}>
                      <Award className="w-6 h-6" />
                    </div>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      b.unlocked ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-800 text-slate-500'
                    }`}>
                      {b.unlocked ? `Unlocked ${b.unlockedAt || ''}` : 'Locked'}
                    </span>
                  </div>

                  <h3 className="text-sm font-bold text-white mt-4">{b.title}</h3>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">{b.description}</p>

                  <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-500 font-mono">
                    <span>Category: {b.category}</span>
                    <span className="text-emerald-400 font-bold">+{b.points} pts</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 8. ADMIN TAB */}
        {activeTab === 'admin' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div>
                <h1 className="text-2xl sm:text-3xl font-black text-white flex items-center gap-2">
                  <Shield className="w-6 h-6 text-amber-400" /> Platform Admin & Analytics
                </h1>
                <p className="text-xs text-slate-400 mt-1">Aggregated platform statistics and registered user roster</p>
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
              <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Total Users</span>
                <div className="text-2xl font-black text-white mt-1">128</div>
              </div>
              <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
                <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider">Active Users</span>
                <div className="text-2xl font-black text-emerald-400 mt-1">94</div>
              </div>
              <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
                <span className="text-[10px] font-bold text-cyan-400 uppercase tracking-wider">AI Plans Made</span>
                <div className="text-2xl font-black text-cyan-400 mt-1">342</div>
              </div>
              <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
                <span className="text-[10px] font-bold text-amber-400 uppercase tracking-wider">Adaptations</span>
                <div className="text-2xl font-black text-amber-400 mt-1">189</div>
              </div>
              <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
                <span className="text-[10px] font-bold text-purple-400 uppercase tracking-wider">Completed</span>
                <div className="text-2xl font-black text-purple-400 mt-1">812</div>
              </div>
              <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800">
                <span className="text-[10px] font-bold text-rose-400 uppercase tracking-wider">Feedbacks</span>
                <div className="text-2xl font-black text-rose-400 mt-1">4.9 ★</div>
              </div>
            </div>

            <div className="p-4 bg-slate-900 border border-slate-800 rounded-2xl">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold text-white">Registered User Directory</h3>
                <div className="relative w-64">
                  <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    placeholder="Search users..."
                    value={adminUserSearch}
                    onChange={e => setAdminUserSearch(e.target.value)}
                    className="w-full pl-8 pr-3 py-1.5 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white"
                  />
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="border-b border-slate-800 text-slate-400 uppercase font-semibold text-[10px]">
                    <tr>
                      <th className="py-2 px-3">Name</th>
                      <th className="py-2 px-3">Goal</th>
                      <th className="py-2 px-3">Level</th>
                      <th className="py-2 px-3">Joined</th>
                      <th className="py-2 px-3">Role</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 text-slate-300">
                    {[
                      { name: user.fullName, email: user.email, goal: user.fitnessGoal, level: user.fitnessLevel, joined: 'Sep 2026', role: 'Admin' },
                      { name: 'Maya Lin', email: 'maya@example.com', goal: 'Weight management', level: 'Beginner', joined: 'Sep 2026', role: 'Member' },
                      { name: 'Karthik Raja', email: 'karthik@example.com', goal: 'Strength', level: 'Intermediate', joined: 'Aug 2026', role: 'Member' },
                      { name: 'Sarah Connor', email: 'sarah@example.com', goal: 'Endurance', level: 'Advanced', joined: 'Aug 2026', role: 'Member' }
                    ]
                      .filter(u => u.name.toLowerCase().includes(adminUserSearch.toLowerCase()) || u.goal.toLowerCase().includes(adminUserSearch.toLowerCase()))
                      .map((u, i) => (
                        <tr key={i} className="hover:bg-slate-800/40">
                          <td className="py-3 px-3">
                            <strong className="text-white block">{u.name}</strong>
                            <span className="text-[10px] text-slate-500">{u.email}</span>
                          </td>
                          <td className="py-3 px-3">{u.goal}</td>
                          <td className="py-3 px-3">
                            <span className="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300">{u.level}</span>
                          </td>
                          <td className="py-3 px-3 text-slate-500 font-mono text-[11px]">{u.joined}</td>
                          <td className="py-3 px-3">
                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${u.role === 'Admin' ? 'bg-amber-500/10 text-amber-400' : 'bg-slate-800 text-slate-400'}`}>
                              {u.role}
                            </span>
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* 9. PROFILE & SETTINGS TAB */}
        {activeTab === 'profile' && (
          <div className="max-w-2xl mx-auto space-y-6">
            <div className="pb-4 border-b border-slate-800">
              <h1 className="text-2xl font-bold text-white">Profile & Preferences</h1>
              <p className="text-xs text-slate-400 mt-1">
                Updating your metrics recalibrates the AI workout and nutritional engines
              </p>
            </div>

            <form
              onSubmit={e => {
                e.preventDefault();
                showToast('Profile updated! New metrics saved.');
              }}
              className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4"
            >
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Full Name</label>
                  <input
                    type="text"
                    value={user.fullName}
                    onChange={e => setUser({ ...user, fullName: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Age</label>
                  <input
                    type="number"
                    value={user.age}
                    onChange={e => setUser({ ...user, age: parseInt(e.target.value) || 25 })}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Height (cm)</label>
                  <input
                    type="number"
                    value={user.height}
                    onChange={e => setUser({ ...user, height: parseFloat(e.target.value) || 170 })}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Weight (kg)</label>
                  <input
                    type="number"
                    step="0.5"
                    value={user.weight}
                    onChange={e => setUser({ ...user, weight: parseFloat(e.target.value) || 70 })}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Fitness Goal</label>
                  <select
                    value={user.fitnessGoal}
                    onChange={e => setUser({ ...user, fitnessGoal: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white"
                  >
                    <option value="Weight management">Weight management</option>
                    <option value="Muscle building & Wellness">Muscle building & Wellness</option>
                    <option value="Strength">Strength</option>
                    <option value="Endurance">Endurance</option>
                    <option value="General wellness">General wellness</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Fitness Level</label>
                  <select
                    value={user.fitnessLevel}
                    onChange={e => setUser({ ...user, fitnessLevel: e.target.value as any })}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white"
                  >
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Dietary Preference</label>
                  <select
                    value={user.dietaryPreference}
                    onChange={e => setUser({ ...user, dietaryPreference: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white"
                  >
                    <option value="Vegetarian">Vegetarian</option>
                    <option value="Non-vegetarian">Non-vegetarian</option>
                    <option value="Vegan">Vegan</option>
                    <option value="Eggetarian">Eggetarian</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Preferred Language</label>
                  <select
                    value={user.preferredLanguage}
                    onChange={e => setUser({ ...user, preferredLanguage: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white"
                  >
                    <option value="English">English</option>
                    <option value="Tamil">Tamil (தமிழ்)</option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold rounded-xl text-xs shadow-md transition"
              >
                Save Preferences
              </button>
            </form>
          </div>
        )}
      </main>

      {/* Adapt Plan Modal */}
      {adaptModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-lg w-full shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Sliders className="w-4 h-4 text-emerald-400" /> Adapt Plan with Gemini AI
              </h3>
              <button onClick={() => setAdaptModalOpen(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>
            <p className="text-xs text-slate-400 mt-2">
              Tell FitBuddy what adjustments to make. Gemini will rewrite the 7-day routine safely.
            </p>

            <div className="flex flex-wrap gap-2 my-4">
              {[
                'Make the workouts easier',
                'Only 30 minutes',
                'Add more cardio',
                'Add yoga & mobility',
                'Remove jumping exercises'
              ].map((chip, idx) => (
                <button
                  key={idx}
                  onClick={() => setAdaptFeedback(chip)}
                  className="px-2.5 py-1 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px] border border-slate-700"
                >
                  {chip}
                </button>
              ))}
            </div>

            <textarea
              rows={3}
              value={adaptFeedback}
              onChange={e => setAdaptFeedback(e.target.value)}
              placeholder="e.g. Lower body volume is too intense, add more core focus instead."
              className="w-full p-3 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-emerald-500"
            />

            <div className="mt-4 flex justify-end gap-2">
              <button
                onClick={() => setAdaptModalOpen(false)}
                className="px-4 py-2 text-xs font-semibold text-slate-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={handleAdaptPlan}
                disabled={isAdapting}
                className="px-5 py-2 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-slate-950 font-bold text-xs rounded-xl shadow-md transition"
              >
                {isAdapting ? 'Adapting with Gemini...' : 'Apply Adaptation'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Exercise Guide Modal */}
      {selectedExercise && (
        <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-xl w-full max-h-[85vh] overflow-y-auto shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Dumbbell className="w-5 h-5 text-emerald-400" /> {selectedExercise.name} Form Guide
              </h3>
              <button onClick={() => setSelectedExercise(null)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            {isGuideLoading ? (
              <div className="py-12 text-center text-xs text-slate-400 flex flex-col items-center gap-2">
                <Sparkles className="w-6 h-6 text-emerald-400 animate-spin" />
                <span>Consulting Gemini AI on biomechanical cues...</span>
              </div>
            ) : exerciseGuide ? (
              <div className="mt-4 space-y-4 text-xs text-slate-300">
                <div>
                  <h4 className="font-bold text-emerald-400 uppercase text-[10px] tracking-wider mb-1">Target & Purpose</h4>
                  <p className="text-slate-300 leading-relaxed">{exerciseGuide.purpose}</p>
                </div>
                <div>
                  <h4 className="font-bold text-cyan-400 uppercase text-[10px] tracking-wider mb-1">Step-by-Step Cues</h4>
                  <ol className="list-decimal pl-4 space-y-1 text-slate-300">
                    {(exerciseGuide.instructions || []).map((step: string, i: number) => (
                      <li key={i}>{step}</li>
                    ))}
                  </ol>
                </div>
                <div>
                  <h4 className="font-bold text-amber-400 uppercase text-[10px] tracking-wider mb-1">Common Mistakes</h4>
                  <ul className="list-disc pl-4 space-y-1 text-slate-300">
                    {(exerciseGuide.commonMistakes || []).map((m: string, i: number) => (
                      <li key={i}>{m}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="font-bold text-emerald-400 uppercase text-[10px] tracking-wider mb-1">Beginner Regression</h4>
                  <p className="text-slate-300">{exerciseGuide.beginnerModification}</p>
                </div>
                <div className="p-3 rounded-lg bg-red-950/30 border border-red-900/40 text-red-300 text-[11px]">
                  <strong>Joint Safety Notice:</strong> {exerciseGuide.safetyNotes}
                </div>
              </div>
            ) : null}
          </div>
        </div>
      )}

      {/* Daily Check-In Modal */}
      {checkInModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-md w-full shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Activity className="w-4 h-4 text-emerald-400" /> Daily Wellness Check-In
              </h3>
              <button onClick={() => setCheckInModalOpen(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={handleCheckInSubmit} className="space-y-4 mt-4 text-xs">
              <div>
                <label className="block text-slate-300 mb-1 font-medium">Energy Level (1 = Low, 5 = Peak)</label>
                <input type="range" name="energy" min="1" max="5" defaultValue="4" className="w-full accent-emerald-500" />
                <div className="flex justify-between text-[10px] text-slate-500">
                  <span>1 (Exhausted)</span>
                  <span>3 (Normal)</span>
                  <span>5 (Energized)</span>
                </div>
              </div>
              <div>
                <label className="block text-slate-300 mb-1 font-medium">Muscle Soreness</label>
                <select name="soreness" className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-white">
                  <option value="None">None</option>
                  <option value="Mild" selected>Mild</option>
                  <option value="Moderate">Moderate</option>
                  <option value="High">High</option>
                </select>
              </div>
              <div>
                <label className="block text-slate-300 mb-1 font-medium">Mood</label>
                <select name="mood" className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-white">
                  <option value="Energetic">Energetic</option>
                  <option value="Good" selected>Good</option>
                  <option value="Calm">Calm</option>
                  <option value="Tired">Tired</option>
                  <option value="Stressed">Stressed</option>
                </select>
              </div>
              <button
                type="submit"
                className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold rounded-xl shadow-md transition"
              >
                Submit & Update AI Recovery Advice
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Platform Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950 py-6 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-slate-300">FitBuddy Platform</span>
            <span>• Full-Stack AI/ML Wellness Architecture</span>
          </div>
          <div className="flex items-center space-x-4 text-[11px]">
            <span>FastAPI + SQLite</span>
            <span>Google Gemini AI</span>
            <span>English / தமிழ் Multilingual</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
