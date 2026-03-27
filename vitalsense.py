"""
InsightCare — Your Personal Health Companion
Flask Application
Run: python vitalsense.py
"""

from flask import Flask, render_template, request, jsonify
from biological_age import calculate_biological_age

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    age       = float(data.get("age", 32))
    sleep     = float(data.get("sleep", 7))
    steps     = float(data.get("steps", 8000))
    stress    = float(data.get("stress", 5))
    systolic  = float(data.get("systolic", 120))
    diastolic = float(data.get("diastolic", 80))
    diet      = float(data.get("diet", 6))
    exercise  = float(data.get("exercise", 150))
    weight    = float(data.get("weight", 70))
    height    = float(data.get("height", 170))
    smoker    = bool(int(data.get("smoker", 0)))

    age_data = {
        "age": age,
        "weight_kg": weight,
        "height_cm": height,
        "sleep_hours": sleep,
        "steps_per_day": steps,
        "stress_level": stress,
        "systolic_bp": systolic,
        "diastolic_bp": diastolic,
        "exercise_min_week": exercise,
        "diet_quality": diet,
        "smoker": smoker,
        "alcohol_units_week": float(data.get("alcohol", 0))
    }

    result = calculate_biological_age(age_data)
    bio_age = result["biological_age"]
    delta = round(bio_age - age, 1)

    if bio_age > age + 3:
        risk_level = "High"
    elif bio_age > age:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    top_risks = []
    if sleep < 6:
        top_risks.append("Poor sleep quality")
    if stress > 7:
        top_risks.append("High stress levels")
    if steps < 5000:
        top_risks.append("Low physical activity")
    if systolic > 130:
        top_risks.append("Elevated blood pressure")
    if diet < 5:
        top_risks.append("Poor diet quality")

    driver_candidates = [
        ("High stress", max(0, (stress - 5) * 0.8)),
        ("Low steps", max(0, (10000 - steps) / 10000 * 2)),
        ("Low sleep", max(0, (7 - sleep) * 0.5)),
        ("Suboptimal diet", max(0, (5 - diet) * 0.4)),
        ("Low exercise", max(0, (150 - exercise) / 150 * 1.2)),
        ("Elevated systolic BP", max(0, (systolic - 120) * 0.12))
    ]

    drivers_sorted = sorted(driver_candidates, key=lambda x: x[1], reverse=True)
    top_drivers = [
        {"label": label, "delta": round(val, 2)} for label,val in drivers_sorted if val > 0
    ][:3]

    return jsonify({
        "biological_age": bio_age,
        "chronological_age": age,
        "delta": delta,
        "risk_level": risk_level,
        "cardio_risk": result["cardio_risk"],
        "metabolic_risk": result["metabolic_risk"],
        "cognitive_risk": result["cognitive_risk"],
        "top_risks": top_risks[:3],
        "top_drivers": top_drivers,
        "percent_younger": int(max(45, min(95, 68 - delta * 2)))
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
