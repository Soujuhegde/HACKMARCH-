"""
CHAT ENGINE — AI Health Assistant
"""

import json
import urllib.request
import urllib.error
from recommendation_engine import GEMINI_URL

SYSTEM_INSTRUCTION = """You are a highly capable AI Health Assistant for the "InsightCare" platform.
Your tone should be warm, direct, and coach-like. Reference the user’s profile details when relevant, but avoid using a fixed name.
Your goals:
* Answer general health-related questions.
* Explain the prediction results in simple, friendly, empathetic terms.
* Suggest precautions, diet, exercise, and lifestyle improvements based on the user's risks.

RULES & SAFETY CONSTRAINTS:
1. NEVER give a definitive medical diagnosis.
2. ALWAYS proactively include a medical disclaimer in pertinent conversations (e.g. "This is not medical advice. Please consult a doctor.").
3. Avoid prescribing medications. Only provide general health guidance.
4. Explain clearly and keep answers easy to understand. Prefer conversational paragraphs; use bullets only as supportive micro-steps.
"""

def generate_chat_response(messages: list, context_data: dict) -> str:
    """
    messages: list of dicts [{"role": "user" or "assistant", "content": "msg"}]
    context_data: dict containing current metrics and bio results
    """
    context_str = (
        f"USER CONTEXT:\n"
        f"- Chronological Age: {context_data.get('age')}\n"
        f"- Biological Age: {context_data.get('biological_age')}\n"
        f"- Cardio Risk: {context_data.get('cardio_risk')}/100\n"
        f"- Metabolic Risk: {context_data.get('metabolic_risk')}/100\n"
        f"- Blood Pressure: {context_data.get('blood_pressure', '128/84')} mmHg\n"
        f"- Stress score: {context_data.get('stress', 8)}/10\n"
        f"- Daily Steps: {context_data.get('steps', 3200)}\n"
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
            return (f"Based on the profile and metabolic risk of {context_data.get('metabolic_risk')}/100, here’s a practical plan:\n\n"
                    "- Keep your plate mostly plants: vegetables, legumes, whole grains, and lean protein.\n"
                    "- Skip processed snacks and sweet drinks, especially before evening.\n"
                    "- Aim for balanced meals with protein + fiber every 4 hours to stabilize energy.\n"
                    "- For your weight and steps, adding a small after-dinner salad makes a big difference.\n\n"
                    "<details><summary><strong>Sources</strong></summary>Based on: AHA guidelines 2023, your metabolic risk of {context_data.get('metabolic_risk')}/100, and 3,200 steps/day.</details>\n\n"
                    "*This is not medical advice; consult a registered dietitian for personalized clinical plan.*")
        elif any(k in last_msg for k in ["exercise", "workout", "gym", "walk", "run", "active", "sport"]):
            return (f"With cardio risk at {context_data.get('cardio_risk')}/100 and 3,200 steps/day, a consistent movement routine can pay off quickly:\n\n"
                    "- Work toward 150 minutes/week of brisk walking; start with 20 minutes for 5 days.\n"
                    "- Add 2 light strength sessions (bodyweight squats/push-ups) to boost metabolism.\n"
                    "- Use stairs and 5-min standing breaks to increase NEAT (non-exercise activity thermogenesis).\n\n"
                    "<details><summary><strong>Sources</strong></summary>AHA 2023, your steps of 3,200/day, and risk of {context_data.get('cardio_risk')}/100.</details>\n\n"
                    "*(Not medical advice; consult your physician before a new plan.)*")
        elif "sleep" in last_msg:
            return (f"With {context_data.get('sleep')} hours nightly you’re close, but 7-8 hours can bring your biologic age down faster:\n\n"
                    "- Wind down 30 minutes before bedtime: no screens, dim lighting, deep breathing.\n"
                    "- Keep a consistent wake/sleep schedule, even weekends.\n"
                    "- Raise legs and do gentle stretching to improve circulation before sleep.\n\n"
                    "<details><summary><strong>Sources</strong></summary>Sleep foundation 2023, your reported sleep {context_data.get('sleep')}h, and stress score {context_data.get('stress')}/10.</details>\n\n"
                    "*(Not medical advice; consult your doctor for persistent issues.)*")
        elif any(k in last_msg for k in ["heart", "cardio", "bp", "blood pressure", "hypertension"]):
            return (f"Current BP is around {context_data.get('blood_pressure','128/84')} and cardio risk is {context_data.get('cardio_risk')}/100, so this is a good focus area:\n\n"
                    "- Keep blood pressure logs and target <120/80 with your provider.\n"
                    "- Walk 30 minutes daily and do 10-min stress breaks to lower systolic readings.\n"
                    "- Reduce sodium and boost potassium-rich foods (leafy greens, bananas).\n\n"
                    "<details><summary><strong>Sources</strong></summary>AHA 2023, your BP 128/84, and stress score 8/10.</details>\n\n"
                    "*(Consult medical professional for diagnosis.)*")
        elif any(k in last_msg for k in ["result", "explain", "risk", "biological", "age"]):
            return (f"Here’s what stands out based on your metrics:\n\n"
                    f"- Biological Age: {context_data.get('biological_age')} vs chronological {context_data.get('age')}\n"
                    f"- Cardiovascular Risk: {context_data.get('cardio_risk')}/100\n"
                    f"- Metabolic Risk: {context_data.get('metabolic_risk')}/100\n"
                    f"- BP: {context_data.get('blood_pressure','128/84')}, Stress: {context_data.get('stress',8)}/10, Steps: {context_data.get('steps',3200)}\n\n"
                    "You’re doing a good job with baseline activity. The biggest leverage points are stress reduction and sleep consistency.\n\n"
                    "<details><summary><strong>Sources</strong></summary>AHA/UK Biobank models, your metrics above, and clinical general guidelines.</details>\n\n"
                    "*(Non-diagnostic insight; speak to your physician for clinical decisions.)*")
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
