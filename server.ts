import express from 'express';
import { createServer as createViteServer } from 'vite';
import dotenv from 'dotenv';
import { GoogleGenAI } from '@google/genai';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = Number(process.env.PORT) || 3000;

app.use(express.json());

// Initialize Google Gemini Client (Server-side only)
const apiKey = process.env.GEMINI_API_KEY || '';
const ai = new GoogleGenAI({
  apiKey,
  httpOptions: {
    headers: {
      'User-Agent': 'aistudio-build',
    }
  }
});

// Helper for calling Gemini
async function callGemini(prompt: string, systemInstruction: string = ''): Promise<string | null> {
  if (!apiKey) {
    return null;
  }
  try {
    const config: any = {};
    if (systemInstruction) {
      config.systemInstruction = systemInstruction;
    }
    const response = await ai.models.generateContent({
      model: 'gemini-3.8-flash',
      contents: prompt,
      config
    });
    return response.text || null;
  } catch (err) {
    console.error('Gemini API invocation error:', err);
    return null;
  }
}

// 1. Workout Generation Endpoint
app.post('/api/gemini/generate-workout', async (req, res) => {
  try {
    const profile = req.body;
    const prompt = `
Generate a structured 7-day personalized workout routine for:
- Goal: ${profile.fitnessGoal || 'General wellness'}
- Level: ${profile.fitnessLevel || 'Beginner'}
- Equipment: ${profile.equipment || 'Dumbbells, Bodyweight'}
- Session Duration: ${profile.preferredDuration || 45} mins
- Intensity: ${profile.preferredIntensity || 'Moderate'}
- Days/week: ${profile.availableDays || 4}

Return ONLY a strict JSON array of 7 day objects (Monday through Sunday) with keys:
- day: string (e.g. "Monday")
- dayNumber: integer (1-7)
- focus: string
- warmup: string
- exercises: array of objects with {exercise, sets, reps, rest, notes}
- cooldown: string
- recoverySuggestion: string
- completed: boolean (false)
Include rest / active recovery days for non-training days.
`;
    const system = 'You are a certified master fitness coach. Output strict valid JSON only without markdown fences.';
    const result = await callGemini(prompt, system);

    if (result) {
      let cleaned = result.trim();
      if (cleaned.startsWith('```json')) cleaned = cleaned.slice(7);
      if (cleaned.startsWith('```')) cleaned = cleaned.slice(3);
      if (cleaned.endsWith('```')) cleaned = cleaned.slice(0, -3);
      try {
        const parsed = JSON.parse(cleaned.trim());
        return res.json({ success: true, plan: parsed });
      } catch (parseErr) {
        console.warn('JSON parse error:', parseErr);
      }
    }
    return res.json({ success: false, message: 'Fallback to deterministic plan' });
  } catch (e: any) {
    res.status(500).json({ error: e.message });
  }
});

// 2. Workout Adaptation Endpoint
app.post('/api/gemini/adapt-workout', async (req, res) => {
  try {
    const { currentPlan, feedback, profile } = req.body;
    const prompt = `
User Feedback: "${feedback}"
Current 7-Day Plan: ${JSON.stringify(currentPlan)}
User Profile: Level ${profile?.fitnessLevel || 'Beginner'}, Goal ${profile?.fitnessGoal || 'Wellness'}.

Modify the 7-day workout plan to address the user's feedback (e.g. "make it easier", "only 30 minutes", "add yoga", "remove jumping exercises").
Maintain good exercise science and safety. Return ONLY a valid JSON array of the 7 updated days with the same structure.
`;
    const system = 'You are a certified fitness coach. Output strict valid JSON only without markdown formatting.';
    const result = await callGemini(prompt, system);

    if (result) {
      let cleaned = result.trim();
      if (cleaned.startsWith('```json')) cleaned = cleaned.slice(7);
      if (cleaned.startsWith('```')) cleaned = cleaned.slice(3);
      if (cleaned.endsWith('```')) cleaned = cleaned.slice(0, -3);
      try {
        const parsed = JSON.parse(cleaned.trim());
        return res.json({ success: true, plan: parsed });
      } catch (parseErr) {
        console.warn('JSON parse error:', parseErr);
      }
    }
    return res.json({ success: false, message: 'Fallback to programmatic adaptation' });
  } catch (e: any) {
    res.status(500).json({ error: e.message });
  }
});

// 3. Exercise Explanation Endpoint
app.post('/api/gemini/explain-exercise', async (req, res) => {
  try {
    const { exerciseName } = req.body;
    const prompt = `
Explain how to perform '${exerciseName}' safely and effectively.
Safety constraint: General fitness guidance only. Do not diagnose injuries or joint disorders.
Return JSON with:
- "purpose": short paragraph on muscular targets
- "instructions": array of 4 chronological steps
- "commonMistakes": array of 3 mistakes
- "beginnerModification": easier variation
- "safetyNotes": safety advice
`;
    const system = 'You are an exercise biomechanics specialist. Output strict JSON only.';
    const result = await callGemini(prompt, system);

    if (result) {
      let cleaned = result.trim();
      if (cleaned.startsWith('```json')) cleaned = cleaned.slice(7);
      if (cleaned.startsWith('```')) cleaned = cleaned.slice(3);
      if (cleaned.endsWith('```')) cleaned = cleaned.slice(0, -3);
      try {
        const parsed = JSON.parse(cleaned.trim());
        return res.json({ success: true, data: parsed });
      } catch (e) {}
    }
    return res.json({
      success: true,
      data: {
        purpose: `Builds functional strength and motor control targeting the primary muscle groups for ${exerciseName}.`,
        instructions: [
          'Assume a stable starting position with core braced and spine neutral.',
          'Initiate the movement with controlled breathing and tempo.',
          'Move through a full comfortable range of motion without joint hyperextension.',
          'Return smoothly to starting posture and repeat with strict form.'
        ],
        commonMistakes: [
          'Using excessive momentum instead of muscular contraction.',
          'Holding breath during the strenuous portion of the rep.',
          'Allowing lumbar spine or shoulders to round.'
        ],
        beginnerModification: 'Reduce external load or leverage, or use support until muscular control is established.',
        safetyNotes: 'Stop immediately if you experience sharp or radiating joint pain.'
      }
    });
  } catch (e: any) {
    res.status(500).json({ error: e.message });
  }
});

// 4. Multilingual Fitness Chatbot
app.post('/api/gemini/chat', async (req, res) => {
  try {
    const { message, language, userProfile } = req.body;
    const isTamil = (language || '').toLowerCase().includes('tamil');
    const langPrompt = isTamil ? 'Respond in natural, encouraging Tamil (தமிழ்).' : 'Respond in clear, friendly English.';

    const prompt = `
USER PROFILE:
Name: ${userProfile?.fullName || 'Athlete'}
Goal: ${userProfile?.fitnessGoal || 'General wellness'}
Level: ${userProfile?.fitnessLevel || 'Beginner'}
Equipment: ${userProfile?.equipment || 'Dumbbells, Bodyweight'}

USER QUESTION:
"${message}"

INSTRUCTIONS:
${langPrompt}
Act as FitBuddy AI Coach. Provide practical, evidence-based fitness or nutrition advice.
SAFETY NOTICE: Never diagnose medical ailments. If the user mentions chest pain, severe dizziness, or acute injuries, recommend professional medical consultation immediately.
`;
    const reply = await callGemini(prompt, 'You are FitBuddy AI coach.');
    if (reply) {
      return res.json({ reply: reply.trim() });
    }

    if (isTamil) {
      return res.json({
        reply: `வணக்கம் ${userProfile?.fullName || ''}! உங்கள் உடற்பயிற்சி இலக்கு (${userProfile?.fitnessGoal || 'ஆரோக்கியம்'}) அடைய FitBuddy AI தயாராக உள்ளது. சரியான முறையில் பயிற்சி செய்து, போதுமான தண்ணீர் அருந்துங்கள்.`
      });
    }

    return res.json({
      reply: `Hello ${userProfile?.fullName || 'there'}! As your FitBuddy AI Coach, I'm here to keep you consistent with your "${userProfile?.fitnessGoal || 'wellness'}" plan. Remember that consistent effort beats intensity in the long run. What specific exercise or nutrition question can I clarify?`
    });
  } catch (e: any) {
    res.status(500).json({ error: e.message });
  }
});

// 5. Daily Wellness Recommendation
app.post('/api/gemini/daily-recommendation', async (req, res) => {
  try {
    const { checkIn, userProfile } = req.body;
    const prompt = `
Check-In:
- Energy: ${checkIn?.energyLevel || 3}/5
- Soreness: ${checkIn?.muscleSoreness || 'None'}
- Sleep: ${checkIn?.sleepQuality || 'Good'}
- Mood: ${checkIn?.mood || 'Good'}
- Goal: ${userProfile?.fitnessGoal || 'Wellness'}

Provide a 2-sentence actionable daily coaching recommendation on training intensity, mobility, and recovery. No medical diagnoses.
`;
    const reply = await callGemini(prompt);
    if (reply) {
      return res.json({ recommendation: reply.trim() });
    }

    const soreness = (checkIn?.muscleSoreness || '').toLowerCase();
    if (soreness === 'high' || (checkIn?.energyLevel || 3) <= 2) {
      return res.json({
        recommendation: 'Your recovery markers indicate elevated fatigue today. Take an active recovery walk, perform 10 minutes of gentle hip stretching, and ensure an extra glass of water before bed.'
      });
    }
    return res.json({
      recommendation: 'Readiness markers look solid! Maintain good form on your programmed exercises, hit your hydration target, and finish with a 5-minute cooldown.'
    });
  } catch (e: any) {
    res.status(500).json({ error: e.message });
  }
});

// Health endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'FitBuddy Full-Stack AI Platform' });
});

// Mount Vite middleware in development
async function startServer() {
  const isProd = process.env.NODE_ENV === 'production';
  if (!isProd) {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa'
    });
    app.use(vite.middlewares);
  } else {
    app.use(express.static(path.resolve(__dirname, 'dist')));
    app.get('*', (req, res) => {
      res.sendFile(path.resolve(__dirname, 'dist', 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`FitBuddy Server running on port ${PORT}`);
  });
}

startServer();
