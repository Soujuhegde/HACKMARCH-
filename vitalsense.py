"""
InsightCare — Your Personal Health Companion
Flask Application
Run: python vitalsense.py
"""

from flask import Flask, render_template, request, jsonify

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
    diet      = float(data.get("diet", 6))
    exercise  = float(data.get("exercise", 150))

    # Biological age estimation formula
    bio_age = age
    bio_age += (stress - 5) * 0.8
    bio_age -= (sleep - 6) * 0.5
    bio_age -= (steps / 10000) * 2
    bio_age -= (diet - 5) * 0.4
    bio_age -= (exercise / 150) * 1.2
    if systolic > 140:
        bio_age += (systolic - 140) * 0.15

    bio_age = round(max(18, min(90, bio_age)), 1)
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

    return jsonify({
        "biological_age": bio_age,
        "chronological_age": age,
        "delta": delta,
        "risk_level": risk_level,
        "top_risks": top_risks[:3]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
