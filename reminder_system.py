import uuid
from typing import List, Dict, Any

def generate_reminders_from_recs(recommendations: List[Any]) -> List[Dict]:
    reminders = []
    
    for rec in recommendations:
        lower_rec = ""
        desc = ""
        if isinstance(rec, dict):
            # Extract fields from the structured AI recommendation dictionary
            title_text = rec.get("title", "")
            desc = rec.get("starter_plan", rec.get("action", ""))
            lower_rec = f"{title_text} {desc}".lower()
        else:
            desc = str(rec)
            lower_rec = desc.lower()
            
        title = "Health Goal"
        time = "09:00 AM" # Default morning time
        frequency = "Daily"
        
        if "sleep" in lower_rec:
            title = "Sleep Routine"
            time = "09:30 PM"
        elif "water" in lower_rec or "hydration" in lower_rec:
            title = "Hydration Goal"
            time = "10:00 AM"
            frequency = "Daily"
        elif "exercise" in lower_rec or "walk" in lower_rec or "workout" in lower_rec or "move" in lower_rec or "cardio" in lower_rec:
            title = "Exercise / Movement"
            time = "07:30 AM"
        elif "diet" in lower_rec or "eat" in lower_rec or "meal" in lower_rec or "veg" in lower_rec or "salad" in lower_rec:
            title = "Healthy Meal Reminder"
            time = "12:30 PM"
        elif "stress" in lower_rec or "breath" in lower_rec or "mindful" in lower_rec:
            title = "Mindfulness Break"
            time = "02:00 PM"
        else:
            title = "Health Goal Check-in"
            
        reminders.append({
            "id": str(uuid.uuid4())[:8],
            "title": "📌 " + title,
            "description": desc,
            "time": time,
            "frequency": frequency,
            "enabled": True,
            "completed_today": False,
            "type": "AI"
        })
        
    has_water = any("water" in r["title"].lower() or "hydrat" in r["title"].lower() for r in reminders)
    if not has_water:
        reminders.append({
            "id": str(uuid.uuid4())[:8],
            "title": "💧 Drink Water",
            "description": "Stay hydrated! Aim for at least 8 glasses today.",
            "time": "11:00 AM",
            "frequency": "Daily",
            "enabled": True,
            "completed_today": False,
            "type": "AI"
        })
        
    return reminders
