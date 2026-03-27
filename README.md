# GoodAI — AI for Longevity 🧬

> **Predict the future. Own your health.**
> Built for the GoodAI Hackathon

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Claude API key (for AI recommendations)
export ANTHROPIC_API_KEY=your_api_key_here

# 3. Run the app
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
goodai_longevity/
├── app.py                  # Main Streamlit app (The Dashboard)
├── biological_age.py       # Bio age calculator (The Mirror)
├── health_simulator.py     # 10-year projection (The Time Machine)
├── recommendation_engine.py # Claude AI coach (The Coach)
├── requirements.txt
└── README.md
```

---

## 🧠 The Insight Loop

```
1. MEASURE     → User inputs health metrics
2. PREDICT     → Biological age + risk scores calculated
3. SIMULATE    → 10-year health trajectory projected
4. RECOMMEND   → Claude AI generates 3 personalized actions
```

---

## 🎯 Features

- **Biological Age Estimator** — Know how old your body really is
- **Health Future Simulator** — See where your habits take you in 10 years
- **Habit Simulation** — Adjust one slider, watch projections update live
- **AI Coach** — Claude generates clear, measurable action steps
- **Risk Scores** — Cardiovascular, metabolic, cognitive risk (0–100)

---

## 🔑 API Key Setup

The app uses the Anthropic Claude API for AI recommendations.

**Option 1** — Environment variable:
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

**Option 2** — In the app (future: settings sidebar)

Without an API key, the app uses fallback algorithmic recommendations — still fully functional.

---

## 🏆 Hackathon Judging Criteria

| Criteria | Implementation |
|---|---|
| Concept Understanding | Full Insight Loop: Measure → Predict → Simulate → Recommend |
| System Design | Modular Python, Claude API, Streamlit |
| Demonstration | Live input → instant bio age + 10y projection + AI coaching |
| Clarity | Single-flow UX, clear numbers, no jargon |
| Innovation | Real-time habit simulation + biological clock + AI recommendations |

---

## 🔮 Roadmap (Automation Phase)

- [ ] Wearable data ingestion (Fitbit/Apple Health CSV)
- [ ] Daily cron job: auto-update health snapshot
- [ ] Week-over-week trend alerts
- [ ] WhatsApp/Email nudges via API
- [ ] Longitudinal tracking dashboard
