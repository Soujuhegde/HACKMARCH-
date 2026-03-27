"""
InsightCare — AI for Longevity
Main Streamlit Application  (Pastel / Light Theme)
Run: streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time

from biological_age import calculate_biological_age, simulate_optimized_age
from health_simulator import project_health_trajectory, calculate_life_expectancy_bonus
from recommendation_engine import get_ai_recommendations

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="InsightCare — AI for Longevity",
    page_icon="💗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — VitalSense Pastel / Light Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;800&family=Nunito+Sans:wght@400;500;600;700&display=swap');

:root {
    --bg:            #F8F6FF;
    --surface:       #FFFFFF;
    --surface-2:     #F3F0FF;
    --pink:          #FF6B8A;
    --purple:        #A78BFA;
    --peach:         #FFB49A;
    --mint:          #6EE7B7;
    --lilac:         #C4B5FD;
    --text-dark:     #2D2D3A;
    --text-body:     #6B6B8A;
    --text-light:    #A0A0BA;
    --border:        rgba(167,139,250,0.18);
    --shadow:        0 4px 24px rgba(167,139,250,0.12);
    --shadow-hover:  0 12px 40px rgba(167,139,250,0.20);
    --green:         #10B981;
    --red:           #F87171;
    --amber:         #FBBF24;
}

/* ── BASE ── */
html, body, .stApp {
    background-color: var(--bg) !important;
    background-image: radial-gradient(ellipse 900px 600px at 50% -80px, rgba(167,139,250,0.09), transparent) !important;
    color: var(--text-dark) !important;
    font-family: 'Nunito Sans', sans-serif !important;
}
.main .block-container {
    padding: 1.5rem 2rem 4rem !important;
    max-width: 1380px !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
h1, h2, h3, h4 { font-family: 'Nunito', sans-serif !important; color: var(--text-dark) !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--lilac); border-radius: 3px; }

/* ── HEADER ── */
.vs-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.1rem 2rem;
    background: var(--surface);
    border-radius: 20px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    margin-bottom: 1.8rem;
}
.vs-logo-name {
    font-family: 'Nunito', sans-serif;
    font-size: 1.5rem; font-weight: 800;
    color: var(--text-dark);
    letter-spacing: -0.01em;
}
.vs-logo-tag {
    font-size: 0.72rem; color: var(--text-light);
    margin-top: 2px; font-weight: 400;
}
.vs-header-badge {
    background: rgba(255,107,138,0.1);
    border: 1px solid rgba(255,107,138,0.25);
    color: var(--pink);
    padding: 0.3rem 1rem; border-radius: 999px;
    font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.06em; text-transform: uppercase;
}

/* ── STEP PILLS ── */
.step-bar {
    display: flex; align-items: center; gap: 0;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px; padding: 0.5rem 1.2rem;
    margin-bottom: 1.6rem;
    box-shadow: var(--shadow);
}
.step-pill {
    border-radius: 999px; padding: 6px 18px;
    font-size: 0.78rem; font-weight: 600;
    white-space: nowrap;
    background: rgba(167,139,250,0.08);
    color: var(--text-light);
    border: 1px solid var(--border);
}
.step-pill.active {
    background: var(--purple); color: white;
    box-shadow: 0 4px 14px rgba(167,139,250,0.35);
    border-color: transparent;
}
.step-line { width: 24px; height: 1px; background: var(--border); }

/* ── SECTION LABELS ── */
.vs-label {
    display: inline-block;
    background: rgba(255,107,138,0.10); color: var(--pink);
    border-radius: 999px; padding: 4px 14px;
    font-size: 0.69rem; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.vs-title {
    font-family: 'Nunito', sans-serif;
    font-size: 1.7rem; font-weight: 800;
    color: var(--text-dark); line-height: 1.2;
    margin-bottom: 1.2rem;
}

/* ── CARDS ── */
.vs-card {
    background: var(--surface);
    border-radius: 20px; padding: 1.6rem 1.5rem;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    margin-bottom: 1.2rem;
}
.vs-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-hover); }

.vs-card-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 1rem;
}
.vs-icon-wrap {
    width: 34px; height: 34px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px;
}
.icon-lilac { background: rgba(196,181,253,0.22); }
.icon-peach  { background: rgba(255,180,154,0.22); }
.icon-mint   { background: rgba(110,231,183,0.22); }
.icon-pink   { background: rgba(255,107,138,0.12); }

.vs-card-title {
    font-family: 'Nunito', sans-serif;
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.09em; text-transform: uppercase;
    color: var(--text-body);
}
.vs-divider { height: 1px; background: var(--border); margin: 0 0 1rem; }

/* ── SAMPLE BANNER ── */
.vs-sample-banner {
    background: var(--surface);
    border-left: 3px solid var(--pink);
    border-radius: 0 12px 12px 0;
    padding: 0.75rem 1.1rem;
    font-size: 0.85rem; color: var(--text-body);
    line-height: 1.5;
    box-shadow: 0 2px 12px rgba(255,107,138,0.08);
    margin-bottom: 1.2rem;
}
.vs-sample-banner strong { color: var(--text-dark); font-weight: 700; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 14px !important;
    border: 1px solid var(--border) !important;
    padding: 0.3rem !important; gap: 0.25rem !important;
    box-shadow: var(--shadow) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-light) !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.3rem !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 0.87rem !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: var(--purple) !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(167,139,250,0.35) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.4rem !important; }

/* ── INPUTS ── */
.stSlider > div { color: var(--text-dark) !important; }
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--pink) !important;
    border: 2px solid white !important;
    box-shadow: 0 2px 8px rgba(255,107,138,0.3) !important;
}
.stSlider [data-baseweb="slider"] [data-testid="stSliderTrackActive"] {
    background: linear-gradient(to right, var(--pink), var(--purple)) !important;
}
.stNumberInput > div > div > input {
    background: var(--surface-2) !important;
    border: 1.5px solid var(--border) !important;
    color: var(--text-dark) !important;
    border-radius: 12px !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-weight: 600 !important;
}
.stSelectbox > div > div > div {
    background: var(--surface-2) !important;
    border: 1.5px solid var(--border) !important;
    color: var(--text-dark) !important;
    border-radius: 12px !important;
}
label[data-testid="stWidgetLabel"] {
    color: var(--text-body) !important;
    font-size: 0.82rem !important; font-weight: 500 !important;
    font-family: 'Nunito Sans', sans-serif !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #FF6B8A 0%, #A78BFA 100%) !important;
    color: white !important; border: none !important;
    border-radius: 14px !important; padding: 0.75rem 2rem !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important; font-size: 0.97rem !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 6px 24px rgba(255,107,138,0.28) !important;
    transition: all 0.2s !important; width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(255,107,138,0.4) !important;
}

/* ── CHECKBOX ── */
.stCheckbox > label { color: var(--text-dark) !important; font-weight: 500 !important; }
.stCheckbox [data-baseweb="checkbox"] > div:first-child {
    background: var(--pink) !important;
    border-color: var(--pink) !important;
    border-radius: 6px !important;
}

/* ── METRIC / BIO AGE CARDS ── */
.vs-bio-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px; padding: 2rem;
    text-align: center;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}
.vs-bio-title {
    font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.12em; color: var(--text-light);
    font-weight: 600; margin-bottom: 0.4rem;
}
.vs-bio-number {
    font-family: 'Nunito', sans-serif;
    font-size: 4.5rem; font-weight: 800; line-height: 1;
    background: linear-gradient(135deg, #FF6B8A, #A78BFA);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.vs-risk-row {
    display: flex; align-items: center;
    margin-bottom: 0.9rem; gap: 0.9rem;
}
.vs-risk-label {
    font-size: 0.78rem; color: var(--text-body);
    width: 130px; flex-shrink: 0; font-weight: 500;
}
.vs-risk-bg {
    flex: 1; height: 8px; background: rgba(167,139,250,0.12);
    border-radius: 4px; overflow: hidden;
}
.vs-risk-fill { height: 100%; border-radius: 4px; }
.vs-risk-score { font-size: 0.78rem; font-weight: 700; width: 35px; text-align: right; }

/* ── INSIGHT BOX ── */
.vs-insight {
    background: linear-gradient(135deg, rgba(255,107,138,0.07), rgba(167,139,250,0.05));
    border: 1px solid rgba(255,107,138,0.2);
    border-radius: 16px; padding: 1.4rem; margin: 1.2rem 0;
}
.vs-insight-title {
    font-family: 'Nunito', sans-serif;
    font-size: 1.05rem; font-weight: 800;
    color: var(--pink); margin-bottom: 0.4rem;
}

/* ── REC CARDS ── */
.vs-rec-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px; padding: 1.4rem;
    margin-bottom: 1rem; position: relative;
    box-shadow: var(--shadow);
}
.vs-rec-rank {
    position: absolute; top: -11px; left: 1.1rem;
    background: linear-gradient(135deg, #FF6B8A, #A78BFA);
    color: white; width: 26px; height: 26px;
    border-radius: 50%; display: flex;
    align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 700;
}
.vs-rec-title {
    font-family: 'Nunito', sans-serif;
    font-size: 1rem; font-weight: 800;
    color: var(--text-dark); margin-bottom: 0.35rem;
}
.vs-rec-action { font-size: 0.88rem; color: var(--text-body); margin-bottom: 0.7rem; }
.vs-rec-impact {
    background: rgba(110,231,183,0.15);
    border: 1px solid rgba(110,231,183,0.35);
    color: #059669; padding: 0.25rem 0.75rem;
    border-radius: 8px; font-size: 0.78rem; font-weight: 600;
    display: inline-block; margin-bottom: 0.55rem;
}
.vs-rec-plan {
    font-size: 0.78rem; color: var(--text-body);
    background: var(--surface-2);
    padding: 0.55rem 0.8rem; border-radius: 8px;
    border-left: 3px solid var(--purple);
}
.diff-easy   { color: #059669; font-weight: 600; }
.diff-medium { color: #D97706; font-weight: 600; }
.diff-hard   { color: #DC2626; font-weight: 600; }

/* ── METRIC CARDS (projection tab) ── */
.vs-metric {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px; padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
    position: relative; overflow: hidden;
}
.vs-metric::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--pink), var(--purple));
}
.vs-metric-val {
    font-family: 'Nunito', sans-serif;
    font-size: 2.2rem; font-weight: 800; line-height: 1; margin: 0.3rem 0;
}
.vs-metric-label {
    font-size: 0.75rem; color: var(--text-light);
    text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;
}
.vs-metric-unit { font-size: 0.72rem; color: var(--text-light); }

/* ── WEEKLY PLAN BOX ── */
.vs-plan-box {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 16px; padding: 1.1rem;
}
.vs-plan-title {
    font-family: 'Nunito', sans-serif;
    font-size: 0.85rem; font-weight: 800;
    color: var(--purple); margin-bottom: 0.7rem;
}
.vs-plan-item {
    font-size: 0.78rem; color: var(--text-body);
    padding: 0.38rem 0; border-bottom: 1px solid var(--border);
}
.vs-plan-item:last-child { border-bottom: none; }

/* ── EMPTY STATE ── */
.vs-empty {
    text-align: center; padding: 4rem 2rem; color: var(--text-light);
}
.vs-empty-icon { font-size: 2.8rem; margin-bottom: 0.8rem; }
.vs-empty-text {
    font-family: 'Nunito', sans-serif;
    font-size: 1.1rem; font-weight: 700; color: var(--text-light);
}

hr { border-color: var(--border) !important; }
.js-plotly-plot .plotly .bg { fill: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SAMPLE DATA
# ─────────────────────────────────────────────
SAMPLE_PROFILE = {
    "age": 32, "weight_kg": 62, "height_cm": 163,
    "sleep_hours": 5.5, "steps_per_day": 3200, "resting_hr": 82,
    "systolic_bp": 128, "diastolic_bp": 84, "smoker": False,
    "packs_per_day": 0, "stress_level": 8, "exercise_min_week": 40,
    "diet_quality": 5, "alcohol_units_week": 4,
}

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for key, default in [("analyzed", False), ("results", None), ("metrics", None), ("ai_recs", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─────────────────────────────────────────────
# HEADER  (with real generated logo)
# ─────────────────────────────────────────────
import base64 as _b64, os as _os

_logo_path = _os.path.join(_os.path.dirname(__file__), "static", "logo.png")
try:
    with open(_logo_path, "rb") as _f:
        _logo_b64 = _b64.b64encode(_f.read()).decode()
    _logo_tag = f'<img src="data:image/png;base64,{_logo_b64}" style="width:52px;height:52px;object-fit:contain;border-radius:12px;" />'
except Exception:
    _logo_tag = """<svg width="36" height="36" viewBox="0 0 36 36" fill="none">
      <circle cx="18" cy="18" r="18" fill="url(#gf)"/>
      <path d="M10 18 C8 15 8 10 13 10 C15 10 17 12 18 13 C19 12 21 10 23 10 C28 10 28 15 26 18 L18 26 Z" fill="white"/>
      <defs><linearGradient id="gf" x1="0" y1="0" x2="36" y2="36"><stop stop-color="#FF6B8A"/><stop offset="1" stop-color="#A78BFA"/></linearGradient></defs>
    </svg>"""

st.markdown(f"""
<div class="vs-header">
  <div style="display:flex;align-items:center;gap:14px;">
    {_logo_tag}
    <div>
      <div class="vs-logo-name">InsightCare</div>
      <div class="vs-logo-tag">Your personal health companion</div>
    </div>
  </div>
  <div class="vs-header-badge">💗 AI for Longevity</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STEP PROGRESS BAR
# ─────────────────────────────────────────────
st.markdown("""
<div class="step-bar">
  <div class="step-pill active">🧬 Health Input</div>
  <div class="step-line"></div>
  <div class="step-pill">🔬 Biological Age</div>
  <div class="step-line"></div>
  <div class="step-pill">📈 Future Projection</div>
  <div class="step-line"></div>
  <div class="step-pill">🎯 Action Plan</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🧬 Health Input",
    "🔬 Biological Age",
    "📈 Future Projection",
    "🎯 Action Plan",
])

# ═══════════════════════════════════
# TAB 1 — HEALTH INPUT
# ═══════════════════════════════════
with tab1:
    st.markdown('<div class="vs-label">STEP 01 · DATA COLLECTION</div>', unsafe_allow_html=True)
    st.markdown('<div class="vs-title">Enter Your Health Data</div>', unsafe_allow_html=True)

    use_sample = st.checkbox("🚀 Use sample profile — Riya, 32", value=True)
    if use_sample:
        st.markdown("""
        <div class="vs-sample-banner">
          <strong>Sample loaded:</strong> Riya, 32 · Sedentary job · Poor sleep · High stress.
          Edit any value below.
        </div>""", unsafe_allow_html=True)

    defaults = SAMPLE_PROFILE if use_sample else {k: None for k in SAMPLE_PROFILE}

    col1, col2, col3 = st.columns(3, gap="medium")

    # ── Personal Info ──
    with col1:
        st.markdown("""
        <div class="vs-card-header">
          <div class="vs-icon-wrap icon-lilac">👤</div>
          <span class="vs-card-title">Personal Info</span>
        </div>
        <div class="vs-divider"></div>""", unsafe_allow_html=True)

        age    = st.number_input("Age (years)",    18, 100,  defaults.get("age", 30) or 30)
        weight = st.number_input("Weight (kg)",    30.0, 200.0, float(defaults.get("weight_kg", 70) or 70))
        height = st.number_input("Height (cm)",    120, 220,  defaults.get("height_cm", 170) or 170)
        smoker = st.checkbox("Smoker 🚬",          value=defaults.get("smoker", False))
        packs  = st.slider("Packs per day", 0.0, 3.0, float(defaults.get("packs_per_day", 0.5)), 0.5) if smoker else 0.0

    # ── Vitals ──
    with col2:
        st.markdown("""
        <div class="vs-card-header">
          <div class="vs-icon-wrap icon-peach">💓</div>
          <span class="vs-card-title">Vitals</span>
        </div>
        <div class="vs-divider"></div>""", unsafe_allow_html=True)

        resting_hr = st.slider("Resting Heart Rate (bpm)", 40, 120, defaults.get("resting_hr", 72) or 72)
        systolic   = st.slider("Systolic BP (mmHg)",       90, 200, defaults.get("systolic_bp", 120) or 120)
        diastolic  = st.slider("Diastolic BP (mmHg)",      60, 130, defaults.get("diastolic_bp", 80) or 80)
        alcohol    = st.slider("Alcohol (units/week)",      0,  50,  defaults.get("alcohol_units_week", 0) or 0)

    # ── Lifestyle ──
    with col3:
        st.markdown("""
        <div class="vs-card-header">
          <div class="vs-icon-wrap icon-mint">🏃</div>
          <span class="vs-card-title">Lifestyle</span>
        </div>
        <div class="vs-divider"></div>""", unsafe_allow_html=True)

        sleep    = st.slider("Sleep (hours/night)",   3.0, 12.0, float(defaults.get("sleep_hours", 7.0) or 7.0), 0.5)
        steps    = st.slider("Daily Steps",           0, 20000,  defaults.get("steps_per_day", 7500) or 7500, 250)
        exercise = st.slider("Exercise (min/week)",   0, 600,    defaults.get("exercise_min_week", 150) or 150)
        stress   = st.slider("Stress Level (1–10)",   1, 10,     defaults.get("stress_level", 5) or 5)
        diet     = st.slider("Diet Quality (1–10)",   1, 10,     defaults.get("diet_quality", 6) or 6)

    st.markdown("<br>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        analyze = st.button("🔬  Analyze My Health", use_container_width=True)

    if analyze:
        metrics = {
            "age": age, "weight_kg": weight, "height_cm": height,
            "sleep_hours": sleep, "steps_per_day": steps, "resting_hr": resting_hr,
            "systolic_bp": systolic, "diastolic_bp": diastolic,
            "smoker": smoker, "packs_per_day": packs,
            "stress_level": stress, "exercise_min_week": exercise,
            "diet_quality": diet, "alcohol_units_week": alcohol,
        }
        with st.spinner("💗 Calculating your health profile…"):
            bio_result = calculate_biological_age(metrics)
            projection = project_health_trajectory(metrics)
        with st.spinner("✨ Generating personalised recommendations…"):
            try:
                ai_recs = get_ai_recommendations(metrics, bio_result)
            except Exception:
                from recommendation_engine import get_fallback_recommendations
                ai_recs = get_fallback_recommendations(metrics, bio_result)

        st.session_state.analyzed = True
        st.session_state.results  = {"bio": bio_result, "projection": projection}
        st.session_state.metrics  = metrics
        st.session_state.ai_recs  = ai_recs
        st.success("✅ Analysis complete! Switch to the other tabs to see your results.")

# ═══════════════════════════════════
# TAB 2 — BIOLOGICAL AGE
# ═══════════════════════════════════
with tab2:
    if not st.session_state.analyzed:
        st.markdown("""
        <div class="vs-empty">
          <div class="vs-empty-icon">🔬</div>
          <div class="vs-empty-text">Complete Step 1 to reveal your Biological Age</div>
        </div>""", unsafe_allow_html=True)
    else:
        bio     = st.session_state.results["bio"]
        metrics = st.session_state.metrics

        st.markdown('<div class="vs-label">THE MIRROR</div>', unsafe_allow_html=True)
        st.markdown('<div class="vs-title">Your Biological Age</div>', unsafe_allow_html=True)

        col_left, col_right = st.columns([1, 1.8], gap="large")

        with col_left:
            delta  = bio["age_delta"]
            s_col  = "#F87171" if delta > 2 else "#10B981" if delta < -1 else "#FBBF24"
            s_text = (f"⚠️ {abs(delta):.1f} yrs older than your age" if delta > 2 else
                      f"✅ {abs(delta):.1f} yrs younger"             if delta < -1 else
                      f"📊 {abs(delta):.1f} yrs — right on track")

            st.markdown(f"""
            <div class="vs-bio-card">
              <div class="vs-bio-title">Biological Age</div>
              <div class="vs-bio-number">{bio['biological_age']}</div>
              <div style="font-size:0.82rem;color:var(--text-light);margin:0.3rem 0;">
                vs chronological age &nbsp;<strong style="color:var(--text-dark);">{bio['chronological_age']}</strong>
              </div>
              <div style="color:{s_col};font-size:0.82rem;font-weight:700;margin-top:0.4rem;">{s_text}</div>
              <div style="margin-top:0.8rem;font-size:0.72rem;color:var(--text-light);">BMI: {bio['bmi']}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown("**Risk Assessment**")
            for risk_name, risk_val, risk_color in [
                ("Cardiovascular",  bio["cardio_risk"],    "#F87171"),
                ("Metabolic",       bio["metabolic_risk"], "#FBBF24"),
                ("Cognitive Decline", bio["cognitive_risk"], "#A78BFA"),
            ]:
                st.markdown(f"""
                <div class="vs-risk-row">
                  <div class="vs-risk-label">{risk_name}</div>
                  <div class="vs-risk-bg">
                    <div class="vs-risk-fill" style="width:{risk_val}%;background:{risk_color};"></div>
                  </div>
                  <div class="vs-risk-score" style="color:{risk_color};">{risk_val}</div>
                </div>""", unsafe_allow_html=True)

        with col_right:
            # Gauge chart — light theme
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=bio["biological_age"],
                delta={
                    "reference": bio["chronological_age"],
                    "increasing": {"color": "#F87171"},
                    "decreasing": {"color": "#10B981"},
                    "valueformat": ".1f",
                },
                title={"text": "Biological vs Chronological Age", "font": {"size": 13, "color": "#A0A0BA"}},
                number={"font": {"size": 52, "color": "#FF6B8A", "family": "Nunito"}},
                gauge={
                    "axis": {"range": [max(0, bio["chronological_age"] - 20), bio["chronological_age"] + 20],
                             "tickcolor": "#C4B5FD", "tickfont": {"color": "#A0A0BA"}},
                    "bar":  {"color": "#A78BFA", "thickness": 0.28},
                    "bgcolor": "#F8F6FF", "bordercolor": "rgba(167,139,250,0.18)",
                    "steps": [
                        {"range": [max(0, bio["chronological_age"]-20), bio["chronological_age"]-2], "color": "rgba(110,231,183,0.12)"},
                        {"range": [bio["chronological_age"]-2, bio["chronological_age"]+2],          "color": "rgba(251,191,36,0.12)"},
                        {"range": [bio["chronological_age"]+2, bio["chronological_age"]+20],         "color": "rgba(248,113,113,0.12)"},
                    ],
                    "threshold": {"line": {"color": "#FBBF24", "width": 3}, "thickness": 0.9, "value": bio["chronological_age"]},
                },
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#6B6B8A", "family": "Nunito Sans"},
                height=300,
                margin=dict(t=40, b=0, l=30, r=30),
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Radar chart — pastel palette
            breakdown  = bio["breakdown"]
            categories = ["Sleep", "Steps", "Blood Pressure", "Heart Rate", "Exercise", "Stress", "Diet"]
            keys       = ["sleep", "steps", "bp", "hr", "exercise", "stress", "diet"]
            scores_pct = [max(0, 100 - (breakdown[k]["score"] / 8 * 100)) for k in keys]

            fig_radar = go.Figure(go.Scatterpolar(
                r=scores_pct, theta=categories,
                fill="toself",
                fillcolor="rgba(255,107,138,0.12)",
                line=dict(color="#FF6B8A", width=2),
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100],
                                    tickfont={"color": "#A0A0BA"}, gridcolor="rgba(167,139,250,0.15)"),
                    angularaxis=dict(tickfont={"color": "#6B6B8A"}, gridcolor="rgba(167,139,250,0.15)"),
                    bgcolor="rgba(0,0,0,0)",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False, height=300,
                margin=dict(t=30, b=30, l=30, r=30),
            )
            st.plotly_chart(fig_radar, use_container_width=True)

# ═══════════════════════════════════
# TAB 3 — FUTURE PROJECTION
# ═══════════════════════════════════
with tab3:
    if not st.session_state.analyzed:
        st.markdown("""
        <div class="vs-empty">
          <div class="vs-empty-icon">📈</div>
          <div class="vs-empty-text">Complete Step 1 to simulate your Health Future</div>
        </div>""", unsafe_allow_html=True)
    else:
        proj    = st.session_state.results["projection"]
        metrics = st.session_state.metrics

        st.markdown('<div class="vs-label">THE TIME MACHINE</div>', unsafe_allow_html=True)
        st.markdown('<div class="vs-title">Your Health in 2035</div>', unsafe_allow_html=True)

        habit_label = proj.get("best_habit_label", "improve sleep")
        st.markdown(f"""
        <div class="vs-insight">
          <div class="vs-insight-title">💡 Single Best Change</div>
          <div style="color:var(--text-body);">If you only change one thing: <strong style="color:var(--purple);">{habit_label}</strong></div>
          <div style="color:#059669;font-size:0.87rem;margin-top:0.4rem;font-weight:600;">
            → Save {proj['age_savings']} years of biological aging &nbsp;·&nbsp; Cut heart risk by {proj['cardio_risk_reduction']} points
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("**🔧 Simulate a Habit Change**")
        c1, c2 = st.columns(2)
        with c1:
            sim_sleep = st.slider("Sleep hours", 3.0, 12.0, float(metrics["sleep_hours"]), 0.5, key="sim_sleep")
        with c2:
            sim_steps = st.slider("Daily steps", 0, 20000, metrics["steps_per_day"], 500, key="sim_steps")

        sim_proj = project_health_trajectory({**metrics, "sleep_hours": sim_sleep, "steps_per_day": sim_steps})

        # Projection line chart — light theme
        fig_proj = go.Figure()
        fig_proj.add_trace(go.Scatter(
            x=proj["years"], y=proj["current_bio_ages"], name="Current Path",
            line=dict(color="#F87171", width=3, dash="dash"),
            fill="tozeroy", fillcolor="rgba(248,113,113,0.05)",
        ))
        fig_proj.add_trace(go.Scatter(
            x=sim_proj["years"], y=sim_proj["optimized_bio_ages"], name="Optimised Path",
            line=dict(color="#A78BFA", width=3),
            fill="tozeroy", fillcolor="rgba(167,139,250,0.08)",
        ))
        fig_proj.add_vline(x=0, line_dash="dot", line_color="#C4B5FD", annotation_text="Today")
        fig_proj.update_layout(
            title=dict(text="Biological Age Projection (10 Years)", font=dict(color="#A0A0BA", size=13)),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,246,255,0.8)",
            font=dict(color="#6B6B8A", family="Nunito Sans"),
            xaxis=dict(title="Years from now", gridcolor="rgba(167,139,250,0.12)", color="#A0A0BA"),
            yaxis=dict(title="Biological Age", gridcolor="rgba(167,139,250,0.12)", color="#A0A0BA"),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#6B6B8A")),
            height=340, margin=dict(t=50, b=50, l=50, r=30),
        )
        st.plotly_chart(fig_proj, use_container_width=True)

        # Cardio risk bar chart
        fig_cardio = go.Figure()
        fig_cardio.add_trace(go.Bar(
            x=proj["years"][::2], y=proj["current_cardio_risk"][::2],
            name="Current Risk", marker_color="rgba(248,113,113,0.65)",
        ))
        fig_cardio.add_trace(go.Bar(
            x=sim_proj["years"][::2], y=sim_proj["optimized_cardio_risk"][::2],
            name="Optimised Risk", marker_color="rgba(167,139,250,0.65)",
        ))
        fig_cardio.update_layout(
            title=dict(text="Cardiovascular Risk Score (0–100)", font=dict(color="#A0A0BA", size=13)),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,246,255,0.8)",
            font=dict(color="#6B6B8A", family="Nunito Sans"),
            xaxis=dict(title="Years from now", gridcolor="rgba(167,139,250,0.12)", color="#A0A0BA"),
            yaxis=dict(title="Risk Score", range=[0, 100], gridcolor="rgba(167,139,250,0.12)", color="#A0A0BA"),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#6B6B8A")),
            barmode="group", height=300, margin=dict(t=50, b=50, l=50, r=30),
        )
        st.plotly_chart(fig_cardio, use_container_width=True)

        m1, m2, m3, m4 = st.columns(4)
        for col, (label, val, unit, color) in zip(
            [m1, m2, m3, m4],
            [
                ("Bio Age Now",              str(proj["current_result"]["biological_age"]),        "years",        "#FF6B8A"),
                ("Bio Age in 10y (current)", str(proj["current_bio_ages"][-1]),                   "years",        "#F87171"),
                ("Bio Age in 10y (opt.)",    str(sim_proj["optimized_bio_ages"][-1]),             "years",        "#10B981"),
                ("Years Saved",              str(round(proj["current_bio_ages"][-1] - sim_proj["optimized_bio_ages"][-1], 1)), "years younger", "#FBBF24"),
            ],
        ):
            with col:
                st.markdown(f"""
                <div class="vs-metric">
                  <div class="vs-metric-label">{label}</div>
                  <div class="vs-metric-val" style="color:{color};">{val}</div>
                  <div class="vs-metric-unit">{unit}</div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════
# TAB 4 — ACTION PLAN
# ═══════════════════════════════════
with tab4:
    if not st.session_state.analyzed:
        st.markdown("""
        <div class="vs-empty">
          <div class="vs-empty-icon">🎯</div>
          <div class="vs-empty-text">Complete Step 1 to get your personalised Action Plan</div>
        </div>""", unsafe_allow_html=True)
    else:
        ai_recs = st.session_state.ai_recs
        bio     = st.session_state.results["bio"]

        st.markdown('<div class="vs-label">THE COACH</div>', unsafe_allow_html=True)
        st.markdown('<div class="vs-title">Your Next Best Actions</div>', unsafe_allow_html=True)

        summary     = ai_recs.get("summary", "")
        biggest_win = ai_recs.get("biggest_win", "")
        if summary:
            st.markdown(f"""
            <div class="vs-insight">
              <div class="vs-insight-title">✨ AI Health Summary</div>
              <div style="color:var(--text-body);font-size:0.93rem;">{summary}</div>
              <div style="margin-top:0.6rem;color:var(--purple);font-size:0.83rem;font-weight:700;">
                ⚡ Biggest Win: {biggest_win}
              </div>
            </div>""", unsafe_allow_html=True)

        recs = ai_recs.get("recommendations", [])
        col_r, col_chart = st.columns([1.3, 0.7], gap="large")

        with col_r:
            for rec in recs[:3]:
                diff       = rec.get("difficulty", "Medium")
                diff_class = f"diff-{diff.lower()}"
                impact_s   = rec.get("impact_score", 7)
                st.markdown(f"""
                <div class="vs-rec-card">
                  <div class="vs-rec-rank">{rec.get('rank','?')}</div>
                  <div class="vs-rec-title">{rec.get('emoji','💡')} {rec.get('title','Action')}</div>
                  <div class="vs-rec-action">{rec.get('action','')}</div>
                  <div class="vs-rec-impact">📈 {rec.get('impact','Improves health')}</div>
                  <div class="vs-rec-plan">📅 {rec.get('starter_plan','')}</div>
                  <div style="margin-top:0.5rem;font-size:0.73rem;color:var(--text-light);">
                    Difficulty: <span class="{diff_class}">{diff}</span>
                    &nbsp;·&nbsp;
                    Impact: <span style="color:var(--purple);font-weight:700;">{impact_s}/10</span>
                  </div>
                </div>""", unsafe_allow_html=True)

        with col_chart:
            if recs:
                rec_titles  = [r.get("title", f"Action {i+1}") for i, r in enumerate(recs[:3])]
                imp_scores  = [r.get("impact_score", 7) for r in recs[:3]]
                difficulties= [r.get("difficulty", "Medium") for r in recs[:3]]
                diff_colors = {"Easy": "#10B981", "Medium": "#FBBF24", "Hard": "#F87171"}
                bar_cols    = [diff_colors.get(d, "#A78BFA") for d in difficulties]

                fig_imp = go.Figure(go.Bar(
                    x=rec_titles, y=imp_scores,
                    marker_color=bar_cols,
                    text=imp_scores, textposition="auto",
                    textfont=dict(color="white", family="Nunito", size=14),
                ))
                fig_imp.update_layout(
                    title=dict(text="Impact Score", font=dict(color="#A0A0BA", size=12)),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,246,255,0.8)",
                    font=dict(color="#6B6B8A", family="Nunito Sans"),
                    xaxis=dict(showgrid=False, color="#A0A0BA"),
                    yaxis=dict(range=[0, 10], gridcolor="rgba(167,139,250,0.12)", color="#A0A0BA"),
                    height=230, margin=dict(t=40, b=40, l=20, r=20),
                    showlegend=False,
                )
                st.plotly_chart(fig_imp, use_container_width=True)

            st.markdown('<div class="vs-plan-box"><div class="vs-plan-title">📋 This Week\'s Micro-Plan</div>', unsafe_allow_html=True)
            for rec in recs[:3]:
                plan = rec.get("starter_plan", "")
                if plan:
                    st.markdown(f'<div class="vs-plan-item">{rec.get("emoji","💡")} {plan}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        _, col_re, _ = st.columns([1, 2, 1])
        with col_re:
            if st.button("🔄 Re-analyse with New Data", use_container_width=True):
                st.session_state.analyzed = False
                st.rerun()
