import pandas as pd
import json
import os
from datetime import datetime

PROFILES_JSON = "profiles.json"
WEARABLE_CSV = "mock_wearable.csv"

def save_profile(metrics: dict, user_id: str = "default_user"):
    """
    Saves user health profile metrics to a local JSON file.
    """
    profiles = {}
    if os.path.exists(PROFILES_JSON):
        try:
            with open(PROFILES_JSON, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    profiles = json.loads(content)
        except json.JSONDecodeError:
            profiles = {}
            
    metrics["last_updated"] = datetime.now().isoformat()
    profiles[user_id] = metrics
    
    with open(PROFILES_JSON, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=4)

def load_profile(user_id: str = "default_user") -> dict:
    """
    Loads user health profile from a local JSON file.
    Returns None if not found.
    """
    if os.path.exists(PROFILES_JSON):
        try:
            with open(PROFILES_JSON, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    profiles = json.loads(content)
                    return profiles.get(user_id)
        except json.JSONDecodeError:
            return None
    return None

def fetch_wearable_data() -> dict:
    """
    Simulates fetching data from a wearable by reading the mock CSV.
    Averages the values to provide a current baseline for steps, sleep, and HR.
    """
    if not os.path.exists(WEARABLE_CSV):
        return None
        
    try:
        df = pd.read_csv(WEARABLE_CSV)
        if df.empty:
            return None
            
        # Calculate recent averages
        avg_steps = int(df["steps"].mean())
        avg_sleep = round(df["sleep_hours"].mean(), 1)
        avg_hr = int(df["resting_hr"].mean())
        
        return {
            "steps_per_day": avg_steps,
            "sleep_hours": avg_sleep,
            "resting_hr": avg_hr,
            "wearable_connected": True
        }
    except Exception as e:
        print(f"Error reading wearable CSV: {e}")
        return None
