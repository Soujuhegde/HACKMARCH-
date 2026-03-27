"""
CHAT ENGINE — AI Health Assistant
"""

import json
import urllib.request
import urllib.error
from recommendation_engine import GEMINI_URL

SYSTEM_INSTRUCTION = """You are a highly capable AI Health Assistant for the "InsightCare" platform.
Your goals:
* Answer general health-related questions.
* Explain the prediction results in simple, friendly, empathetic terms.
* Suggest precautions, diet, exercise, and lifestyle improvements based on the user's risks.

RULES & SAFETY CONSTRAINTS:
1. NEVER give a definitive medical diagnosis.
2. ALWAYS proactively include a medical disclaimer in pertinent conversations (e.g. "This is not medical advice. Please consult a doctor.").
3. Avoid prescribing medications. Only provide general health guidance.
4. Explain clearly and keep answers easy to understand. Use bullet points for suggestions if helpful.
"""

def generate_chat_response(messages: list, context_data: dict) -> str:
    """
    messages: list of dicts [{"role": "user" or "assistant", "content": "msg"}]
    context_data: dict containing current metrics and bio results
    """
    context_str = (
        f"USER CONTEXT:\n- Chronological Age: {context_data.get('age')}\n"
        f"- Biological Age: {context_data.get('biological_age')}\n"
        f"- Cardio Risk: {context_data.get('cardio_risk')}/100\n"
        f"- Metabolic Risk: {context_data.get('metabolic_risk')}/100\n"
        f"- Sleep: {context_data.get('sleep')} hrs/night"
    )

    contents = []
    
    for i, msg in enumerate(messages):
        role = "user" if msg["role"] == "user" else "model"
        text = msg["content"]
        
        # Inject system prompt into the first message only
        if i == 0 and role == "user":
            text = f"{SYSTEM_INSTRUCTION}\n\n{context_str}\n\nUser Question: {text}"
            
        contents.append({
            "role": role,
            "parts": [{"text": text}]
        })
        
    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 800,
        }
    }
    
    req = urllib.request.Request(
        GEMINI_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            candidates = result.get("candidates", [])
            if candidates:
                return candidates[0]["content"]["parts"][0]["text"]
            return "I'm sorry, I couldn't generate a response."
    except Exception as e:
        # Fallback to context-aware logic for ANY API issue (429, 403, 404, etc.)
        last_msg = messages[-1]["content"].lower()
        if any(k in last_msg for k in ["diet", "food", "nutrition", "eat", "meal"]):
            return (f"Regarding your diet and Metabolic Risk of {context_data.get('metabolic_risk')}/100:\n\n"
                    "- Try a **Mediterranean-style diet** (high in vegetables, whole grains, and lean proteins).\n"
                    "- Reduce ultra-processed foods and sugary drinks.\n"
                    "- Drink **2-3 liters of water** a day.\n"
                    "- Focusing on low-glycemic foods is highly recommended for your profile.\n\n"
                    "*(Note: Always consult a dietitian for medical advice).*")
        elif any(k in last_msg for k in ["exercise", "workout", "gym", "walk", "run", "active", "sport"]):
            return (f"For your heart health and Cardiovascular Risk of {context_data.get('cardio_risk')}/100:\n\n"
                    "- Aim for **150 minutes** of moderate aerobic activity per week (like brisk walking).\n"
                    "- Add **2 days of strength training** to improve metabolic health.\n"
                    "- Stretch daily to reduce stress.\n\n"
                    "*(Note: Please consult a doctor before starting new exercises).*")
        elif "sleep" in last_msg:
            return ("Here are some tips to improve your sleep quality:\n\n"
                    f"- Current habits: {context_data.get('sleep')} hours. Aim for **7.5 to 8 hours** per night.\n"
                    "- Keep your room cool (65\u00b0F / 18\u00b0C) and dark.\n"
                    "- Avoid screens an hour before bed.\n\n"
                    "*(Note: Consult a physician if insomnia persists).*")
        elif any(k in last_msg for k in ["heart", "cardio", "bp", "blood pressure", "hypertension"]):
            return (f"Regarding your Cardiovascular Risk ({context_data.get('cardio_risk')}/100):\n\n"
                    "- **Monitor Blood Pressure:** Aim for a target below 120/80 mmHg.\n"
                    "- **Aerobic Exercise:** 30 mins of brisk walking daily is highly effective.\n"
                    "- **Sodium Intake:** Lowering salt helps improve your blood pressure profile.\n\n"
                    "*(Note: Cardiovascular concerns require professional medical monitoring.)*")
        elif any(k in last_msg for k in ["result", "explain", "risk", "biological", "age"]):
            return (f"Here's a summary of your health data:\n\n"
                    f"- **Biological Age:** {context_data.get('biological_age')} (vs actual age of {context_data.get('age')})\n"
                    f"- **Cardiovascular Risk:** {context_data.get('cardio_risk')}/100\n"
                    f"- **Metabolic Risk:** {context_data.get('metabolic_risk')}/100\n\n"
                    f"Your biological age is {'higher' if context_data.get('biological_age',0) > context_data.get('age',0) else 'lower'} than your chronological age. "
                    "Focus on sleep and stress management for the best results.\n\n"
                    "*(Disclaimer: This is not a medical diagnosis.)*")
        elif any(k in last_msg for k in ["smok", "tobacco", "cigarette", "vape"]):
            return ("To help reduce your health risks:\n\n"
                    "- Set a **quit date** and tell friends for accountability.\n"
                    "- Use nicotine replacement therapy if needed (consult your doctor).\n"
                    "- Replace the habit with healthy alternatives like walking.\n\n"
                    "*(Note: Please consult a healthcare provider for a plan.)*")
        elif any(k in last_msg for k in ["stress", "anxiety", "mental", "relax"]):
            return ("To manage your stress effectively:\n\n"
                    "- Practice **deep breathing** for 5-10 minutes daily.\n"
                    "- Maintain a consistent sleep-wake schedule.\n"
                    "- Exercise regularly to balance cortisol levels.\n\n"
                    "*(Note: Speak with a mental health professional for support.)*")
        else:
            # Most generic fallback that still includes real data
            return (f"Based on your profile (Bio Age: {context_data.get('biological_age')}), here's what I can share:\n\n"
                    "I'm currently focused on providing guidance on your specific results. "
                    "Ask me about **diet**, **exercise**, **heart health**, or **explain your results** for tailored advice.\n\n"
                    "*(Please consult a doctor for serious concerns.)*")
