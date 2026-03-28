def validate_metrics(metrics):
    """
    Validates health metrics against realistic and clinical standards.
    Returns: (errors, warnings, confidence)
    """
    errors = []
    warnings = []
    confidence = 100

    # 1. HARD INPUT VALIDATION (ERRORS)
    if metrics["age"] < 18 or metrics["age"] > 110:
        errors.append("❌ Age must be between 18 and 110 for clinical accuracy.")

    if metrics["systolic_bp"] < 70 or metrics["systolic_bp"] > 230:
        errors.append("❌ Systolic Blood Pressure looks unrealistic (70–230 mmHg).")

    if metrics["diastolic_bp"] < 40 or metrics["diastolic_bp"] > 140:
        errors.append("❌ Diastolic Blood Pressure looks unrealistic (40–140 mmHg).")

    if metrics["sleep_hours"] < 2 or metrics["sleep_hours"] > 15:
        errors.append("❌ Sleep duration must be between 2 and 15 hours.")

    if metrics["steps_per_day"] < 0:
        errors.append("❌ Steps cannot be negative.")

    # 2. CLINICAL VALIDATION (WARNINGS)
    if metrics["systolic_bp"] >= 140 or metrics["diastolic_bp"] >= 90:
        warnings.append("⚠️ Stage 2 Hypertension detected. Consult a healthcare provider.")
        confidence -= 5
    elif metrics["systolic_bp"] >= 130 or metrics["diastolic_bp"] >= 80:
        warnings.append("⚠️ Elevated Blood Pressure (Stage 1 Hypertension).")
        confidence -= 2

    if metrics["resting_hr"] > 100:
        warnings.append("⚠️ Tachycardia (High Resting HR) detected (>100 bpm).")
        confidence -= 5
    elif metrics["resting_hr"] < 50:
        warnings.append("⚠️ Low Heart Rate (Bradycardia) detected. Monitor if you feel dizzy.")

    if metrics["sleep_hours"] < 6:
        warnings.append("⚠️ Severe sleep deficiency (<6 hours) accelerates aging.")
        confidence -= 10

    if metrics["stress_level"] >= 8:
        warnings.append("⚠️ High chronic stress affects prediction confidence.")
        confidence -= 10

    # 3. CROSS-FIELD VALIDATION (CONSISTENCY)
    if metrics["steps_per_day"] > 18000 and metrics["exercise_min_week"] < 30:
        warnings.append("⚖️ High daily steps but very low exercise? Data may be inconsistent.")
        confidence -= 5

    if metrics["age"] > 60 and metrics["resting_hr"] < 45:
        warnings.append("⚖️ Very low heart rate for age — ensure metrics are from a medical device.")
        confidence -= 3

    # Ensure confidence doesn't drop too low for valid but risky data
    confidence = max(40, confidence)

    return errors, warnings, confidence
