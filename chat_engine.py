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
    except urllib.error.HTTPError as e:
        if e.code == 429:
            last_msg = messages[-1]["content"].lower()
            if "diet" in last_msg or "food" in last_msg or "road" in last_msg:
                return ("Here are some diet recommendations based on your profile:\n\n"
                        "- Try adopting a **Mediterranean-style diet** (high in vegetables, whole grains, and lean proteins).\n"
                        "- Reduce ultra-processed foods and sugary drinks.\n"
                        "- Drink **2-3 liters of water** a day to improve your metabolic goals.\n\n"
                        "*(Note: Always consult a dietitian for medical advice).*")
            elif "exercise" in last_msg or "workout" in last_msg:
                return ("Here are some exercise recommendations for you!\n\n"
                        "- Start with **150 minutes** of moderate aerobic activity per week (like brisk walking).\n"
                        "- Combine that with **2 days of strength training** to lower your cardiovascular risks.\n"
                        "- Stretch daily to improve flexibility and reduce stress.\n\n"
                        "*(Note: Please consult a doctor before starting new exercises).*")
            elif "sleep" in last_msg:
                return ("Here are some tips to improve your sleep quality:\n\n"
                        "- Aim for **7-9 hours** per night.\n"
                        "- Keep your room cool (65\u00b0F / 18\u00b0C) and dark.\n"
                        "- Avoid screens an hour before bed.\n"
                        "- This will significantly help your cognitive health!\n\n"
                        "*(Note: Consult a physician if insomnia persists).*")
            elif "result" in last_msg or "explain" in last_msg or "risk" in last_msg:
                return (f"Here's a summary of your health data:\n\n"
                        f"- **Biological Age:** {context_data.get('biological_age')} (vs actual age of {context_data.get('age')})\n"
                        f"- **Cardio Risk Score:** {context_data.get('cardio_risk')}/100\n"
                        f"- **Metabolic Risk Score:** {context_data.get('metabolic_risk')}/100\n\n"
                        f"Lowering your stress and improving sleep are the strongest levers to reverse this trajectory.\n\n"
                        f"*(Disclaimer: This is not a medical diagnosis. Please consult a doctor.)*")
            elif "smok" in last_msg or "tobacco" in last_msg or "cigarette" in last_msg:
                return ("Here are some tips to help quit smoking:\n\n"
                        "- Set a **quit date** and tell friends/family for accountability.\n"
                        "- Try **nicotine replacement therapy** (patches, gum) — consult your doctor first.\n"
                        "- Identify your **triggers** and replace the habit with healthy alternatives.\n"
                        "- Stay active — exercise reduces cravings.\n"
                        "- Consider support groups or counseling.\n\n"
                        "*(Note: Please consult a healthcare provider for a personalized quit plan.)*")
            elif "stress" in last_msg or "anxiety" in last_msg or "mental" in last_msg:
                return ("Here are some strategies to manage stress:\n\n"
                        "- Practice **deep breathing exercises** or meditation (even 5 minutes helps).\n"
                        "- Get regular physical activity.\n"
                        "- Maintain a consistent **sleep schedule**.\n"
                        "- Limit caffeine and alcohol intake.\n"
                        "- Talk to someone you trust about your feelings.\n\n"
                        "*(Note: If you're struggling, please reach out to a mental health professional.)*")
            else:
                return (f"Based on your profile, here's what I can share:\n\n"
                        f"- **Chronological Age:** {context_data.get('age')}\n"
                        f"- **Biological Age:** {context_data.get('biological_age')}\n\n"
                        f"Focus on improving your most critical lifestyle factor (often sleep or stress management) for the best results.\n\n"
                        f"Feel free to ask me about **diet**, **exercise**, **sleep**, or **your results**!\n\n"
                        f"*(Please consult a doctor for serious health concerns.)*")
        
        err_msg = e.read().decode('utf-8')
        print(f"Gemini API Error: {e.code} - {err_msg}")
        return "I'm temporarily unavailable. Please try again later. (API Error)"
    except Exception as e:
        print(f"Chat Engine Error: {str(e)}")
        return "An unexpected error occurred. Please try again."
