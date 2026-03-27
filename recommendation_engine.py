"""
THE COACH — Next Best Action Engine
Uses Google Gemini API to generate personalized, actionable health recommendations.
"""

import json
import urllib.request
import urllib.error

GEMINI_API_KEY = "AIzaSyDvam3ohesx6LdqW6-x-p_rP9QfhpZCLxg"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY
)


def get_ai_recommendations(metrics: dict, bio_age_result: dict) -> dict:
    status_tag = (
        "⚠️ OLDER" if bio_age_result["age_delta"] > 2
        else "✅ YOUNGER" if bio_age_result["age_delta"] < -1
        else "ON TRACK"
    )

    prompt = f"""You are a world-class preventive health AI coach. Analyze this person's health data and provide exactly 3 highly personalized, actionable recommendations.

PATIENT HEALTH PROFILE:
- Chronological Age: {metrics['age']} years
- Biological Age: {bio_age_result['biological_age']} years ({status_tag} by {abs(bio_age_result['age_delta'])} years)
- BMI: {bio_age_result['bmi']}
- Sleep: {metrics['sleep_hours']} hours/night
- Daily Steps: {metrics['steps_per_day']:,}
- Resting Heart Rate: {metrics['resting_hr']} bpm
- Blood Pressure: {metrics['systolic_bp']}/{metrics['diastolic_bp']} mmHg
- Stress Level: {metrics['stress_level']}/10
- Exercise: {metrics['exercise_min_week']} min/week
- Diet Quality: {metrics['diet_quality']}/10
- Smoker: {metrics.get('smoker', False)}
- Alcohol: {metrics.get('alcohol_units_week', 0)} units/week

RISK SCORES (0-100):
- Cardiovascular: {bio_age_result['cardio_risk']}
- Metabolic: {bio_age_result['metabolic_risk']}
- Cognitive Decline: {bio_age_result['cognitive_risk']}

Return ONLY valid JSON, no markdown fences, no explanation:
{{
  "recommendations": [
    {{
      "rank": 1,
      "title": "Short title",
      "action": "Specific measurable action",
      "target_metric": "What this improves",
      "impact": "Reduces X risk by Y% / Lowers biological age by Z years",
      "impact_score": <1-10>,
      "starter_plan": "This week: do X every day",
      "difficulty": "Easy|Medium|Hard",
      "emoji": "relevant emoji"
    }}
  ],
  "summary": "One sentence overall health summary",
  "biggest_win": "The single most impactful change today"
}}"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 1200,
        },
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req  = urllib.request.Request(
            GEMINI_URL, data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            text   = result["candidates"][0]["content"]["parts"][0]["text"].strip()

            # Strip any accidental markdown fences
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            text = text.strip()

            return json.loads(text)

    except Exception as e:
        print(f"[Gemini API error] {e}")
        return get_fallback_recommendations(metrics, bio_age_result)


def get_fallback_recommendations(metrics: dict, bio_age_result: dict) -> dict:
    recs = []

    if metrics["sleep_hours"] < 7:
        recs.append({
            "rank": 1, "emoji": "🌙", "title": "Prioritise Sleep",
            "action": f"Increase sleep from {metrics['sleep_hours']}h to 7.5 hours/night",
            "target_metric": "Biological age, stress, immune function",
            "impact": "Reduces biological age by up to 2.5 years",
            "impact_score": 9,
            "starter_plan": "This week: Set a fixed bedtime 30 mins earlier each day",
            "difficulty": "Easy",
        })

    if metrics["steps_per_day"] < 8000:
        recs.append({
            "rank": len(recs) + 1, "emoji": "🚶", "title": "Move More",
            "action": f"Increase daily steps from {metrics['steps_per_day']:,} to 8,000",
            "target_metric": "Cardiovascular health, metabolic rate",
            "impact": "Reduces cardiovascular risk by 18%",
            "impact_score": 8,
            "starter_plan": "This week: Park 1 km farther, always take the stairs",
            "difficulty": "Easy",
        })

    if metrics["stress_level"] >= 7:
        recs.append({
            "rank": len(recs) + 1, "emoji": "🧘", "title": "Lower Stress",
            "action": "10 minutes of mindfulness or box-breathing daily",
            "target_metric": "Cortisol, cognitive health, sleep quality",
            "impact": "Reduces cognitive decline risk by 15%",
            "impact_score": 7,
            "starter_plan": "This week: Box breathing (4-4-4-4) at lunch every day",
            "difficulty": "Easy",
        })

    if metrics["exercise_min_week"] < 150:
        recs.append({
            "rank": len(recs) + 1, "emoji": "🏃", "title": "Exercise Regularly",
            "action": "3 × 30 min moderate cardio per week",
            "target_metric": "Heart health, blood pressure, mood",
            "impact": "Lowers biological age by up to 3 years",
            "impact_score": 9,
            "starter_plan": "Mon / Wed / Fri — 30 min brisk walk after dinner",
            "difficulty": "Medium",
        })

    while len(recs) < 3:
        recs.append({
            "rank": len(recs) + 1, "emoji": "🥗", "title": "Improve Diet",
            "action": "5 servings of vegetables and fruits every day",
            "target_metric": "Metabolic health, inflammation",
            "impact": "Reduces metabolic risk by 12%",
            "impact_score": 7,
            "starter_plan": "This week: Add a salad at lunch every single day",
            "difficulty": "Medium",
        })

    return {
        "recommendations": recs[:3],
        "summary": (
            f"Your biological age is {bio_age_result['biological_age']} vs "
            f"chronological {bio_age_result['chronological_age']}. "
            "Focus on the top recommendation for fastest results."
        ),
        "biggest_win": recs[0]["action"] if recs else "Improve sleep quality",
    }
