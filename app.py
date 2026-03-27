"""
GoodAI — AI for Longevity
Main Streamlit Application
Run: streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
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
    page_title="GoodAI — AI for Longevity",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Dark Theme, Purple Palette
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg-primary: #080B14;
    --bg-card: #0F1422;
    --bg-card2: #151B2E;
    --accent: #7C3AED;
    --accent-light: #A855F7;
    --accent-glow: rgba(124, 58, 237, 0.25);
    --amber: #F59E0B;
    --green: #10B981;
    --red: #EF4444;
    --text-primary: #F1F5F9;
    --text-secondary: #64748B;
    --text-muted: #334155;
    --border: rgba(124, 58, 237, 0.2);
}

/* Global Reset */
html, body, .stApp {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

.main .block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 1400px !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Typography */
h1, h2, h3, h4 { font-family: 'Syne', sans-serif !important; }

/* ── HEADER ── */
.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.2rem 2rem;
    background: linear-gradient(135deg, #0F1422 0%, #151B2E 100%);
    border-radius: 20px;
    border: 1px solid var(--border);
    margin-bottom: 2rem;
    box-shadow: 0 0 40px var(--accent-glow);
}

.logo-text {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #A855F7, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}

.header-tag {
    background: var(--accent-glow);
    border: 1px solid var(--accent);
    color: #A855F7;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── METRIC CARDS ── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent);
}

.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1;
    margin: 0.3rem 0;
}

.metric-label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
}

.metric-delta {
    font-size: 0.85rem;
    font-weight: 600;
    margin-top: 0.3rem;
}

.delta-bad { color: var(--red); }
.delta-good { color: var(--green); }
.delta-neutral { color: var(--amber); }

/* ── BIO AGE RING ── */
.bio-age-container {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 0 60px var(--accent-glow);
    margin-bottom: 1rem;
}

.bio-age-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
}

.bio-age-number {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #A855F7, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}

/* ── RISK BARS ── */
.risk-row {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    gap: 1rem;
}

.risk-label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    width: 130px;
    flex-shrink: 0;
}

.risk-bar-bg {
    flex: 1;
    height: 8px;
    background: var(--text-muted);
    border-radius: 4px;
    overflow: hidden;
}

.risk-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 1s ease;
}

.risk-score {
    font-size: 0.8rem;
    font-weight: 700;
    width: 40px;
    text-align: right;
}

/* ── RECOMMENDATION CARDS ── */
.rec-card {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
}

.rec-rank {
    position: absolute;
    top: -12px; left: 1.2rem;
    background: var(--accent);
    color: white;
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
}

.rec-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

.rec-action {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 0.8rem;
}

.rec-impact {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: var(--green);
    padding: 0.3rem 0.8rem;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 0.6rem;
}

.rec-plan {
    font-size: 0.8rem;
    color: #94A3B8;
    background: rgba(255,255,255,0.03);
    padding: 0.6rem 0.8rem;
    border-radius: 8px;
    border-left: 3px solid var(--accent);
}

.difficulty-easy { color: var(--green); }
.difficulty-medium { color: var(--amber); }
.difficulty-hard { color: var(--red); }

/* ── SECTION HEADERS ── */
.section-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--accent-light);
    font-weight: 600;
    margin-bottom: 0.3rem;
}

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.7rem;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 1.5rem;
    line-height: 1.2;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
    padding: 0.3rem !important;
    gap: 0.3rem !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: 9px !important;
    padding: 0.6rem 1.4rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: white !important;
}

.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.5rem !important;
}

/* ── INPUTS ── */
.stSlider > div { color: var(--text-primary) !important; }
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--accent) !important;
}

.stNumberInput > div > div > input,
.stSelectbox > div > div > div {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
}

label[data-testid="stWidgetLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #A855F7) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2.5rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px var(--accent-glow) !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124,58,237,0.5) !important;
}

/* ── TOGGLE / CHECKBOX ── */
.stCheckbox [data-baseweb="checkbox"] > div {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; }

/* ── INSIGHT SUMMARY BOX ── */
.insight-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(168,85,247,0.05));
    border: 1px solid var(--accent);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1.5rem 0;
}

.insight-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #A855F7;
}

/* ── SAMPLE USER BANNER ── */
.sample-banner {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    font-size: 0.85rem;
    color: var(--amber);
    margin-bottom: 1.5rem;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 3px; }

/* plotly chart backgrounds */
.js-plotly-plot .plotly .bg { fill: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SAMPLE DATA (Riya from the brief)
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
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "results" not in st.session_state:
    st.session_state.results = None
if "metrics" not in st.session_state:
    st.session_state.metrics = None
if "ai_recs" not in st.session_state:
    st.session_state.ai_recs = None

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div>
        <div class="logo-text">⊕ GoodAI</div>
        <div style="font-size:0.75rem; color:#64748B; margin-top:0.2rem;">Predict the future. Own your health.</div>
    </div>
    <div class="header-tag">🧬 AI for Longevity · Hackathon Demo</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Health Input",
    "🪞 Biological Age",
    "⏳ Future Projection",
    "🎯 Action Plan"
])

# ─────────────────────────────────────────────
# TAB 1: INPUT
# ─────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-label">Step 1 — The Collector</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Enter Your Health Data</div>', unsafe_allow_html=True)
    
    use_sample = st.checkbox("🔖 Use sample profile (Riya, 32)", value=True)
    if use_sample:
        st.markdown('<div class="sample-banner">📌 Sample profile loaded: Riya, 32 — sedentary job, poor sleep, high stress. Edit any value below.</div>', unsafe_allow_html=True)
    
    defaults = SAMPLE_PROFILE if use_sample else {k: None for k in SAMPLE_PROFILE}
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**👤 Personal**")
        age = st.number_input("Age (years)", min_value=18, max_value=100,
                              value=defaults.get("age", 30) or 30)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0,
                                  value=float(defaults.get("weight_kg", 70) or 70))
        height = st.number_input("Height (cm)", min_value=120, max_value=220,
                                   value=defaults.get("height_cm", 170) or 170)
        smoker = st.checkbox("Smoker", value=defaults.get("smoker", False))
        if smoker:
            packs = st.slider("Packs per day", 0.0, 3.0,
                              float(defaults.get("packs_per_day", 0.5)), 0.5)
        else:
            packs = 0.0
    
    with col2:
        st.markdown("**💓 Vitals**")
        resting_hr = st.slider("Resting Heart Rate (bpm)", 40, 120,
                                defaults.get("resting_hr", 72) or 72)
        systolic = st.slider("Systolic BP (mmHg)", 90, 200,
                              defaults.get("systolic_bp", 120) or 120)
        diastolic = st.slider("Diastolic BP (mmHg)", 60, 130,
                               defaults.get("diastolic_bp", 80) or 80)
        alcohol = st.slider("Alcohol (units/week)", 0, 50,
                             defaults.get("alcohol_units_week", 0) or 0)
    
    with col3:
        st.markdown("**🏃 Lifestyle**")
        sleep = st.slider("Sleep (hours/night)", 3.0, 12.0,
                          float(defaults.get("sleep_hours", 7.0) or 7.0), 0.5)
        steps = st.slider("Daily Steps", 0, 20000,
                          defaults.get("steps_per_day", 7500) or 7500, 250)
        exercise = st.slider("Exercise (min/week)", 0, 600,
                              defaults.get("exercise_min_week", 150) or 150)
        stress = st.slider("Stress Level (1-10)", 1, 10,
                           defaults.get("stress_level", 5) or 5)
        diet = st.slider("Diet Quality (1-10)", 1, 10,
                         defaults.get("diet_quality", 6) or 6)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        analyze = st.button("🧬 Analyze My Health", use_container_width=True)
    
    if analyze:
        metrics = {
            "age": age, "weight_kg": weight, "height_cm": height,
            "sleep_hours": sleep, "steps_per_day": steps, "resting_hr": resting_hr,
            "systolic_bp": systolic, "diastolic_bp": diastolic,
            "smoker": smoker, "packs_per_day": packs,
            "stress_level": stress, "exercise_min_week": exercise,
            "diet_quality": diet, "alcohol_units_week": alcohol,
        }
        
        with st.spinner("🔬 Analyzing your health profile..."):
            bio_result = calculate_biological_age(metrics)
            projection = project_health_trajectory(metrics)
            
        with st.spinner("🤖 Getting AI recommendations..."):
            try:
                ai_recs = get_ai_recommendations(metrics, bio_result)
            except:
                from recommendation_engine import get_fallback_recommendations
                ai_recs = get_fallback_recommendations(metrics, bio_result)
        
        st.session_state.analyzed = True
        st.session_state.results = {"bio": bio_result, "projection": projection}
        st.session_state.metrics = metrics
        st.session_state.ai_recs = ai_recs
        
        st.success("✅ Analysis complete! Navigate to the other tabs to see your results.")

# ─────────────────────────────────────────────
# TAB 2: BIOLOGICAL AGE
# ─────────────────────────────────────────────
with tab2:
    if not st.session_state.analyzed:
        st.markdown("""
        <div style="text-align:center; padding:4rem; color:#64748B;">
            <div style="font-size:3rem;">🪞</div>
            <div style="font-family:'Syne',sans-serif; font-size:1.3rem; margin-top:1rem;">Complete Step 1 to see your Biological Age</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        bio = st.session_state.results["bio"]
        metrics = st.session_state.metrics
        
        st.markdown('<div class="section-label">The Mirror</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Your Biological Age</div>', unsafe_allow_html=True)
        
        col_main, col_side = st.columns([1, 1.8])
        
        with col_main:
            delta = bio["age_delta"]
            status_color = "#EF4444" if delta > 2 else "#10B981" if delta < -1 else "#F59E0B"
            status_text = f"⚠️ {abs(delta):.1f} years OLDER than your age" if delta > 2 else \
                          f"✅ {abs(delta):.1f} years YOUNGER" if delta < -1 else \
                          f"📊 {abs(delta):.1f} years — On Track"
            
            st.markdown(f"""
            <div class="bio-age-container">
                <div class="bio-age-title">Biological Age</div>
                <div class="bio-age-number">{bio['biological_age']}</div>
                <div style="color:#64748B; font-size:0.9rem; margin:0.3rem 0;">vs chronological age: <strong style="color:#F1F5F9;">{bio['chronological_age']}</strong></div>
                <div style="color:{status_color}; font-size:0.85rem; font-weight:600; margin-top:0.5rem;">{status_text}</div>
                <div style="margin-top:1rem; color:#64748B; font-size:0.75rem;">BMI: {bio['bmi']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Risk Assessment**")
            for risk_name, risk_val, risk_color in [
                ("Cardiovascular", bio["cardio_risk"], "#EF4444"),
                ("Metabolic", bio["metabolic_risk"], "#F59E0B"),
                ("Cognitive Decline", bio["cognitive_risk"], "#A855F7"),
            ]:
                st.markdown(f"""
                <div class="risk-row">
                    <div class="risk-label">{risk_name}</div>
                    <div class="risk-bar-bg">
                        <div class="risk-bar-fill" style="width:{risk_val}%; background:{risk_color};"></div>
                    </div>
                    <div class="risk-score" style="color:{risk_color};">{risk_val}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col_side:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=bio["biological_age"],
                delta={
                    "reference": bio["chronological_age"],
                    "increasing": {"color": "#EF4444"},
                    "decreasing": {"color": "#10B981"},
                    "valueformat": ".1f"
                },
                title={"text": "Biological vs Chronological Age", "font": {"size": 14, "color": "#64748B"}},
                number={"font": {"size": 56, "color": "#A855F7", "family": "Syne"}},
                gauge={
                    "axis": {"range": [max(0, bio["chronological_age"] - 20), bio["chronological_age"] + 20],
                             "tickcolor": "#334155", "tickfont": {"color": "#64748B"}},
                    "bar": {"color": "#7C3AED", "thickness": 0.3},
                    "bgcolor": "#1A1A2E",
                    "bordercolor": "#334155",
                    "steps": [
                        {"range": [max(0, bio["chronological_age"] - 20), bio["chronological_age"] - 2], "color": "rgba(16,185,129,0.15)"},
                        {"range": [bio["chronological_age"] - 2, bio["chronological_age"] + 2], "color": "rgba(245,158,11,0.15)"},
                        {"range": [bio["chronological_age"] + 2, bio["chronological_age"] + 20], "color": "rgba(239,68,68,0.15)"},
                    ],
                    "threshold": {
                        "line": {"color": "#F59E0B", "width": 3},
                        "thickness": 0.9,
                        "value": bio["chronological_age"]
                    }
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#F1F5F9", "family": "DM Sans"},
                height=300,
                margin=dict(t=40, b=0, l=30, r=30)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            breakdown = bio["breakdown"]
            categories = ["Sleep", "Steps", "Blood Pressure", "Heart Rate", "Exercise", "Stress", "Diet"]
            keys = ["sleep", "steps", "bp", "hr", "exercise", "stress", "diet"]
            scores_raw = [breakdown[k]["score"] for k in keys]
            scores_pct = [max(0, 100 - (s / 8 * 100)) for s in scores_raw]
            
            fig_radar = go.Figure(go.Scatterpolar(
                r=scores_pct,
                theta=categories,
                fill='toself',
                fillcolor="rgba(124,58,237,0.2)",
                line=dict(color="#A855F7", width=2),
                name="Your Health"
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], tickfont={"color": "#64748B"}, gridcolor="#1E2A3A"),
                    angularaxis=dict(tickfont={"color": "#94A3B8"}, gridcolor="#1E2A3A"),
                    bgcolor="rgba(0,0,0,0)",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                height=300,
                margin=dict(t=30, b=30, l=30, r=30)
            )
            st.plotly_chart(fig_radar, use_container_width=True)

# ─────────────────────────────────────────────
# TAB 3: FUTURE PROJECTION
# ─────────────────────────────────────────────
with tab3:
    if not st.session_state.analyzed:
        st.markdown("""
        <div style="text-align:center; padding:4rem; color:#64748B;">
            <div style="font-size:3rem;">⏳</div>
            <div style="font-family:'Syne',sans-serif; font-size:1.3rem; margin-top:1rem;">Complete Step 1 to see your Health Future</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        proj = st.session_state.results["projection"]
        metrics = st.session_state.metrics
        
        st.markdown('<div class="section-label">The Time Machine</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Your Health in 2035</div>', unsafe_allow_html=True)
        
        habit_label = proj.get("best_habit_label", "improve sleep")
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">💡 Single Best Change</div>
            <div style="color:#E2E8F0;">If you only change one thing: <strong style="color:#A855F7;">{habit_label}</strong></div>
            <div style="color:#10B981; font-size:0.9rem; margin-top:0.5rem; font-weight:600;">
                → Save {proj['age_savings']} years of biological aging · Cut heart risk by {proj['cardio_risk_reduction']} points
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**🔧 Simulate: Change One Habit**")
        habit_col1, habit_col2 = st.columns(2)
        with habit_col1:
            sim_sleep = st.slider("Sleep hours", 3.0, 12.0, float(metrics["sleep_hours"]), 0.5, key="sim_sleep")
        with habit_col2:
            sim_steps = st.slider("Daily steps", 0, 20000, metrics["steps_per_day"], 500, key="sim_steps")
        
        sim_metrics = {**metrics, "sleep_hours": sim_sleep, "steps_per_day": sim_steps}
        sim_proj = project_health_trajectory(sim_metrics)
        
        fig_proj = go.Figure()
        fig_proj.add_trace(go.Scatter(
            x=proj["years"], y=proj["current_bio_ages"],
            name="Current Path",
            line=dict(color="#EF4444", width=3, dash="dash"),
            fill="tozeroy", fillcolor="rgba(239,68,68,0.05)"
        ))
        fig_proj.add_trace(go.Scatter(
            x=sim_proj["years"], y=sim_proj["optimized_bio_ages"],
            name="Optimized Path",
            line=dict(color="#7C3AED", width=3),
            fill="tozeroy", fillcolor="rgba(124,58,237,0.1)"
        ))
        fig_proj.add_vline(x=0, line_dash="dot", line_color="#64748B", annotation_text="Today")
        fig_proj.update_layout(
            title=dict(text="Biological Age Projection (10 Years)", font=dict(color="#94A3B8", size=13)),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,20,34,0.8)",
            font=dict(color="#F1F5F9", family="DM Sans"),
            xaxis=dict(title="Years from now", gridcolor="#1E2A3A", color="#64748B"),
            yaxis=dict(title="Biological Age", gridcolor="#1E2A3A", color="#64748B"),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94A3B8")),
            height=350, margin=dict(t=50, b=50, l=50, r=30)
        )
        st.plotly_chart(fig_proj, use_container_width=True)
        
        fig_cardio = go.Figure()
        fig_cardio.add_trace(go.Bar(x=proj["years"][::2], y=proj["current_cardio_risk"][::2],
                                    name="Current Risk", marker_color="rgba(239,68,68,0.7)"))
        fig_cardio.add_trace(go.Bar(x=sim_proj["years"][::2], y=sim_proj["optimized_cardio_risk"][::2],
                                    name="Optimized Risk", marker_color="rgba(124,58,237,0.7)"))
        fig_cardio.update_layout(
            title=dict(text="Cardiovascular Risk Score (0–100)", font=dict(color="#94A3B8", size=13)),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,20,34,0.8)",
            font=dict(color="#F1F5F9", family="DM Sans"),
            xaxis=dict(title="Years from now", gridcolor="#1E2A3A", color="#64748B"),
            yaxis=dict(title="Risk Score", range=[0, 100], gridcolor="#1E2A3A", color="#64748B"),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94A3B8")),
            barmode="group", height=300, margin=dict(t=50, b=50, l=50, r=30)
        )
        st.plotly_chart(fig_cardio, use_container_width=True)
        
        c1, c2, c3, c4 = st.columns(4)
        metrics_to_show = [
            ("Bio Age Now", f"{proj['current_result']['biological_age']}", "years", "#A855F7"),
            ("Bio Age in 10y (current)", f"{proj['current_bio_ages'][-1]}", "years", "#EF4444"),
            ("Bio Age in 10y (optimized)", f"{sim_proj['optimized_bio_ages'][-1]}", "years", "#10B981"),
            ("Years Saved", f"{round(proj['current_bio_ages'][-1] - sim_proj['optimized_bio_ages'][-1], 1)}", "years younger", "#F59E0B"),
        ]
        for col, (label, val, unit, color) in zip([c1, c2, c3, c4], metrics_to_show):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="color:{color}; font-size:2rem;">{val}</div>
                    <div style="color:#64748B; font-size:0.75rem;">{unit}</div>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 4: ACTION PLAN
# ─────────────────────────────────────────────
with tab4:
    if not st.session_state.analyzed:
        st.markdown("""
        <div style="text-align:center; padding:4rem; color:#64748B;">
            <div style="font-size:3rem;">🎯</div>
            <div style="font-family:'Syne',sans-serif; font-size:1.3rem; margin-top:1rem;">Complete Step 1 to get your Action Plan</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        ai_recs = st.session_state.ai_recs
        bio = st.session_state.results["bio"]
        
        st.markdown('<div class="section-label">The Coach</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Your Next Best Actions</div>', unsafe_allow_html=True)
        
        summary = ai_recs.get("summary", "")
        biggest_win = ai_recs.get("biggest_win", "")
        
        if summary:
            st.markdown(f"""
            <div class="insight-box">
                <div class="insight-title">🤖 AI Health Summary</div>
                <div style="color:#E2E8F0; font-size:0.95rem;">{summary}</div>
                <div style="margin-top:0.8rem; color:#F59E0B; font-size:0.85rem; font-weight:600;">⚡ Biggest Win: {biggest_win}</div>
            </div>
            """, unsafe_allow_html=True)
        
        recs = ai_recs.get("recommendations", [])
        col_r1, col_r2 = st.columns([1.2, 0.8])
        
        with col_r1:
            for rec in recs[:3]:
                diff = rec.get("difficulty", "Medium")
                diff_class = f"difficulty-{diff.lower()}"
                impact_score = rec.get("impact_score", 7)
                st.markdown(f"""
                <div class="rec-card">
                    <div class="rec-rank">{rec.get('rank', '?')}</div>
                    <div class="rec-title">{rec.get('emoji', '💡')} {rec.get('title', 'Action')}</div>
                    <div class="rec-action">{rec.get('action', '')}</div>
                    <div class="rec-impact">📈 {rec.get('impact', 'Improves health')}</div>
                    <div class="rec-plan">📅 {rec.get('starter_plan', '')}</div>
                    <div style="margin-top:0.6rem; font-size:0.75rem; color:#64748B;">
                        Difficulty: <span class="{diff_class}">{diff}</span> &nbsp;·&nbsp;
                        Impact Score: <span style="color:#A855F7; font-weight:700;">{impact_score}/10</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col_r2:
            if recs:
                rec_titles = [r.get("title", f"Action {i+1}") for i, r in enumerate(recs[:3])]
                impact_scores = [r.get("impact_score", 7) for r in recs[:3]]
                difficulties = [r.get("difficulty", "Medium") for r in recs[:3]]
                diff_colors = {"Easy": "#10B981", "Medium": "#F59E0B", "Hard": "#EF4444"}
                bar_colors = [diff_colors.get(d, "#7C3AED") for d in difficulties]
                
                fig_impact = go.Figure(go.Bar(
                    x=rec_titles, y=impact_scores,
                    marker_color=bar_colors,
                    marker_line_color="rgba(255,255,255,0.1)", marker_line_width=1,
                    text=impact_scores, textposition="auto",
                    textfont=dict(color="white", family="Syne", size=14)
                ))
                fig_impact.update_layout(
                    title=dict(text="Impact Score by Recommendation", font=dict(color="#94A3B8", size=12)),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,20,34,0.8)",
                    font=dict(color="#F1F5F9", family="DM Sans"),
                    xaxis=dict(gridcolor="#1E2A3A", color="#64748B"),
                    yaxis=dict(range=[0, 10], gridcolor="#1E2A3A", color="#64748B"),
                    height=250, margin=dict(t=50, b=50, l=30, r=20), showlegend=False
                )
                st.plotly_chart(fig_impact, use_container_width=True)
            
            st.markdown("""
            <div style="background:#0F1422; border:1px solid rgba(124,58,237,0.2); border-radius:16px; padding:1.2rem;">
                <div style="font-family:'Syne',sans-serif; font-size:0.9rem; font-weight:700; margin-bottom:0.8rem; color:#A855F7;">📋 This Week's Micro-Plan</div>
            """, unsafe_allow_html=True)
            for rec in recs[:3]:
                plan = rec.get("starter_plan", "")
                if plan:
                    st.markdown(f"""
                    <div style="font-size:0.8rem; color:#94A3B8; padding:0.4rem 0; border-bottom:1px solid #1E2A3A;">
                        {rec.get('emoji','💡')} {plan}
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_re1, col_re2, col_re3 = st.columns([1, 2, 1])
        with col_re2:
            if st.button("🔄 Re-analyze with New Data", use_container_width=True):
                st.session_state.analyzed = False
                st.rerun()
