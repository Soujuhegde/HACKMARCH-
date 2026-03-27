"""
THE COACH — Next Best Action Engine
Uses Claude API to generate personalized, actionable health recommendations.
"""

import json
import urllib.request

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

def get_ai_recommendations(metrics: dict, bio_age_result: dict) -> dict:
    """
    Call Claude API to get personalized health recommendations.
    Returns structured recommendations with impact scores.
    """
    
    prompt = f"""You are a world-class preventive health AI coach. Analyze this person's health data and provide exactly 3 highly personalized, actionable recommendations.

PATIENT HEALTH PROFILE:
- Chronological Age: {metrics['age']} years
- Biological Age: {bio_age_result['biological_age']} years ({"⚠️ OLDER" if bio_age_result['age_delta'] > 2 else "✅ YOUNGER" if bio_age_result['age_delta'] < -1 else "ON TRACK"} by {abs(bio_age_result['age_delta'])} years)
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
- Cardiovascular Risk: {bio_age_result['cardio_risk']}
- Metabolic Risk: {bio_age_result['metabolic_risk']}
- Cognitive Decline Risk: {bio_age_result['cognitive_risk']}

Generate EXACTLY 3 recommendations. For each recommendation provide:
1. The specific action (be concrete and measurable, not vague)
2. The health metric it targets
3. Estimated impact: X% reduction in a specific risk, OR X years off biological age
4. A 7-day starter plan (one line)
5. Difficulty: Easy / Medium / Hard

Format your response as valid JSON only, no markdown, no explanation:
{{
  "recommendations": [
    {{
      "rank": 1,
      "title": "Short action title",
      "action": "Specific, measurable action",
      "target_metric": "What this improves",
      "impact": "Reduces cardiovascular risk by X% / Lowers biological age by X years",
      "impact_score": <number 1-10>,
      "starter_plan": "This week: do X every day",
      "difficulty": "Easy|Medium|Hard",
      "emoji": "relevant emoji"
    }}
  ],
  "summary": "One sentence overall health summary for this person",
  "biggest_win": "The single most impactful change this person can make today"
}}"""

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            CLAUDE_API_URL,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            text = result["content"][0]["text"]
            
            # Clean JSON if needed
            text = text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            
            return json.loads(text.strip())
    
    except Exception as e:
        # Fallback recommendations if API fails
        return get_fallback_recommendations(metrics, bio_age_result)

def get_fallback_recommendations(metrics: dict, bio_age_result: dict) -> dict:
    """Algorithmic fallback recommendations when API is unavailable."""
    recs = []
    
    if metrics["sleep_hours"] < 7:
        recs.append({
            "rank": 1,
            "title": "Sleep More",
            "action": f"Increase sleep from {metrics['sleep_hours']}h to 7.5 hours per night",
            "target_metric": "Biological age, stress, immune function",
            "impact": "Reduces biological age by up to 2.5 years",
            "impact_score": 9,
            "starter_plan": "This week: Set a fixed bedtime 30 mins earlier each day",
            "difficulty": "Easy",
            "emoji": "🌙"
        })
    
    if metrics["steps_per_day"] < 8000:
        recs.append({
            "rank": len(recs) + 1,
            "title": "Walk More",
            "action": f"Increase daily steps from {metrics['steps_per_day']:,} to 8,000",
            "target_metric": "Cardiovascular health, metabolic rate",
            "impact": "Reduces cardiovascular risk by 18%",
            "impact_score": 8,
            "starter_plan": "This week: Park 1km farther, take stairs always",
            "difficulty": "Easy",
            "emoji": "🚶"
        })
    
    if metrics["stress_level"] >= 7:
        recs.append({
            "rank": len(recs) + 1,
            "title": "Manage Stress",
            "action": "Practice 10 minutes of mindfulness or breathing daily",
            "target_metric": "Cortisol, cognitive health, sleep quality",
            "impact": "Reduces cognitive decline risk by 15%",
            "impact_score": 7,
            "starter_plan": "This week: Use Headspace or box breathing (4-4-4-4) at lunch",
            "difficulty": "Easy",
            "emoji": "🧘"
        })
    
    if metrics["exercise_min_week"] < 150:
        recs.append({
            "rank": len(recs) + 1,
            "title": "Exercise Regularly",
            "action": "Add 3x30min moderate cardio per week (brisk walk/cycle/swim)",
            "target_metric": "Heart health, blood pressure, mood",
            "impact": "Lowers biological age by up to 3 years",
            "impact_score": 9,
            "starter_plan": "This week: Monday, Wednesday, Friday — 30 min brisk walk",
            "difficulty": "Medium",
            "emoji": "🏃"
        })
    
    # Ensure we have at least 3
    while len(recs) < 3:
        recs.append({
            "rank": len(recs) + 1,
            "title": "Improve Diet",
            "action": "Add 5 servings of vegetables and fruits daily",
            "target_metric": "Metabolic health, inflammation",
            "impact": "Reduces metabolic risk by 12%",
            "impact_score": 7,
            "starter_plan": "This week: Add a salad at lunch every day",
            "difficulty": "Medium",
            "emoji": "🥗"
        })
    
    return {
        "recommendations": recs[:3],
        "summary": f"Your biological age is {bio_age_result['biological_age']} vs chronological {bio_age_result['chronological_age']}. Focus on the top recommendation for fastest results.",
        "biggest_win": recs[0]["action"] if recs else "Improve sleep quality"
    }
