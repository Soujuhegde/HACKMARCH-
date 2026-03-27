"""
THE MIRROR — Biological Age Estimator
Calculates biological age based on health metrics using weighted scoring.
"""

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)

def score_bmi(bmi: float) -> float:
    """Returns age penalty/bonus based on BMI. Optimal BMI=22, returns years added to bio age."""
    if bmi < 18.5:
        return 2.0
    elif 18.5 <= bmi < 25:
        return 0.0  # optimal
    elif 25 <= bmi < 30:
        return 1.5
    elif 30 <= bmi < 35:
        return 4.0
    else:
        return 7.0

def score_sleep(hours: float) -> float:
    if 7 <= hours <= 9:
        return 0.0  # optimal
    elif 6 <= hours < 7 or 9 < hours <= 10:
        return 1.5
    elif 5 <= hours < 6:
        return 3.5
    else:
        return 6.0

def score_steps(steps: int) -> float:
    if steps >= 10000:
        return -1.0  # bonus: actually younger
    elif 7500 <= steps < 10000:
        return 0.0
    elif 5000 <= steps < 7500:
        return 1.5
    elif 2500 <= steps < 5000:
        return 3.5
    else:
        return 6.0

def score_blood_pressure(systolic: int, diastolic: int) -> float:
    if systolic < 120 and diastolic < 80:
        return 0.0  # optimal
    elif 120 <= systolic < 130 and diastolic < 80:
        return 1.0  # elevated
    elif 130 <= systolic < 140 or 80 <= diastolic < 90:
        return 3.0  # stage 1 hypertension
    elif systolic >= 140 or diastolic >= 90:
        return 6.0  # stage 2
    else:
        return 0.0

def score_resting_hr(bpm: int) -> float:
    if 50 <= bpm <= 65:
        return -0.5  # athletic, bonus
    elif 66 <= bpm <= 75:
        return 0.0
    elif 76 <= bpm <= 85:
        return 1.5
    elif 86 <= bpm <= 100:
        return 3.0
    else:
        return 5.0

def score_smoking(smoker: bool, packs_per_day: float = 0) -> float:
    if not smoker:
        return 0.0
    elif packs_per_day <= 0.5:
        return 3.0
    elif packs_per_day <= 1:
        return 5.0
    else:
        return 8.0

def score_stress(level: int) -> float:
    """Stress level 1-10"""
    if level <= 3:
        return 0.0
    elif level <= 5:
        return 1.0
    elif level <= 7:
        return 2.5
    else:
        return 4.5

def score_exercise(minutes_per_week: int) -> float:
    if minutes_per_week >= 300:
        return -1.5  # bonus
    elif minutes_per_week >= 150:
        return 0.0
    elif minutes_per_week >= 75:
        return 1.5
    elif minutes_per_week >= 30:
        return 3.0
    else:
        return 5.0

def score_diet(quality: int) -> float:
    """Diet quality 1-10"""
    if quality >= 8:
        return -0.5
    elif quality >= 6:
        return 0.0
    elif quality >= 4:
        return 1.5
    else:
        return 3.5

def score_alcohol(units_per_week: int) -> float:
    if units_per_week == 0:
        return 0.0
    elif units_per_week <= 7:
        return 0.5
    elif units_per_week <= 14:
        return 2.0
    else:
        return 4.0

def calculate_biological_age(metrics: dict) -> dict:
    """
    Main function. Takes health metrics dict, returns biological age analysis.
    
    metrics keys:
      age, weight_kg, height_cm, sleep_hours, steps_per_day,
      systolic_bp, diastolic_bp, resting_hr, smoker, packs_per_day,
      stress_level, exercise_min_week, diet_quality, alcohol_units_week
    """
    age = metrics["age"]
    bmi = calculate_bmi(metrics["weight_kg"], metrics["height_cm"])
    
    # Weighted penalties (years added to biological age)
    weights = {
        "bmi":      (score_bmi(bmi),                                           0.13),
        "sleep":    (score_sleep(metrics["sleep_hours"]),                       0.15),
        "steps":    (score_steps(metrics["steps_per_day"]),                     0.15),
        "bp":       (score_blood_pressure(metrics["systolic_bp"], metrics["diastolic_bp"]), 0.18),
        "hr":       (score_resting_hr(metrics["resting_hr"]),                   0.09),
        "smoking":  (score_smoking(metrics.get("smoker", False), metrics.get("packs_per_day", 0)), 0.10),
        "stress":   (score_stress(metrics["stress_level"]),                     0.08),
        "exercise": (score_exercise(metrics["exercise_min_week"]),               0.07),
        "diet":     (score_diet(metrics["diet_quality"]),                       0.03),
        "alcohol":  (score_alcohol(metrics.get("alcohol_units_week", 0)),       0.02),
    }
    
    total_penalty = sum(score * weight for score, weight in weights.values())
    # Scale: penalty ranges 0-8, map to age delta -3 to +12 years
    age_delta = (total_penalty / 8.0) * 15 - 3
    biological_age = round(age + age_delta, 1)
    
    # Risk scores (0-100), calibrated to realistic ranges
    cardio_risk = min(95, max(5, int(
        15 +  # baseline
        (weights["bp"][0] / 6.0) * 30 +
        (weights["hr"][0] / 5.0) * 15 +
        (weights["smoking"][0] / 8.0) * 20 +
        (weights["steps"][0] / 6.0) * 10 +
        (weights["exercise"][0] / 5.0) * 10
    )))
    
    metabolic_risk = min(95, max(5, int(
        10 +  # baseline
        (weights["bmi"][0] / 7.0) * 30 +
        (weights["diet"][0] / 3.5) * 20 +
        (weights["sleep"][0] / 6.0) * 15 +
        (weights["alcohol"][0] / 4.0) * 10
    )))
    
    cognitive_risk = min(95, max(5, int(
        10 +  # baseline
        (weights["stress"][0] / 4.5) * 30 +
        (weights["sleep"][0] / 6.0) * 25 +
        (weights["exercise"][0] / 5.0) * 10 +
        (weights["alcohol"][0] / 4.0) * 10
    )))
    
    # Breakdown for display
    breakdown = {k: {"score": round(v[0], 2), "weight": v[1], "contribution": round(v[0] * v[1], 2)} 
                 for k, v in weights.items()}
    
    return {
        "chronological_age": age,
        "biological_age": biological_age,
        "age_delta": round(age_delta, 1),
        "bmi": bmi,
        "total_penalty": round(total_penalty, 2),
        "cardio_risk": cardio_risk,
        "metabolic_risk": metabolic_risk,
        "cognitive_risk": cognitive_risk,
        "breakdown": breakdown,
        "status": "older" if age_delta > 2 else "younger" if age_delta < -1 else "on_track"
    }

def simulate_optimized_age(metrics: dict, habit_changes: dict) -> dict:
    """
    Simulate biological age after changing habits.
    habit_changes: dict of metric overrides e.g. {"sleep_hours": 8, "steps_per_day": 8000}
    """
    optimized = {**metrics, **habit_changes}
    return calculate_biological_age(optimized)
