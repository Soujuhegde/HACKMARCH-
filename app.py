"""
InsightCare — AI for Longevity
Main Streamlit Application  (Pastel / Light Theme)
Run: streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components
import json
import time
from datetime import datetime

from biological_age import calculate_biological_age, simulate_optimized_age
from health_simulator import project_health_trajectory, calculate_life_expectancy_bonus
from recommendation_engine import get_ai_recommendations
from report_generator import create_pdf_report

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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');

:root {
    --dz-bg-grad: #F8FAFC;
    --dz-surface: #FFFFFF;
    --dz-surface-solid: #FFFFFF;
    --dz-text: #0F172A;
    --dz-text-light: #64748B;
    --dz-primary: #063B96;
    --dz-primary-grad: #063B96;
    --dz-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
    --dz-border: #E2E8F0;
    --dz-radius: 20px;
    --dz-glow: 0 0 0 3px rgba(6, 59, 150, 0.2);
}

html, body, .stApp {
    background: var(--dz-bg-grad) !important;
    background-attachment: fixed !important;
    color: var(--dz-text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important; color: #334155 !important;
    letter-spacing: -0.02em !important;
}

.stApp::before {
    content: ''; position: fixed; top: -15%; left: -10%;
    width: 60vw; height: 60vw;
    background: transparent;
    border-radius: 50%; z-index: 0; pointer-events: none;
    animation: dz-float 12s ease-in-out infinite alternate;
}
.stApp::after {
    content: ''; position: fixed; bottom: -10%; right: -15%;
    width: 65vw; height: 65vw;
    background: transparent;
    border-radius: 50%; z-index: 0; pointer-events: none;
    animation: dz-float 15s ease-in-out infinite alternate-reverse;
}
@keyframes dz-float {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(30px, -40px) scale(1.05); }
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.main .block-container {
    padding: 2rem 2.5rem 5rem !important;
    max-width: 1200px !important;
    z-index: 1; position: relative;
    animation: dz-fade 0.8s ease-out forwards;
}
@keyframes dz-fade {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

.vs-card, .vs-bio-card, .vs-insight, .vs-rec-card, .vs-metric, .vs-plan-box, .vs-sample-banner, .vs-header {
    background: var(--dz-surface) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid var(--dz-border) !important;
    border-radius: var(--dz-radius) !important;
    box-shadow: var(--dz-shadow) !important;
    padding: 1.8rem !important;
    margin-bottom: 1.5rem !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}
.vs-card:hover, .vs-rec-card:hover { transform: translateY(-4px) !important; box-shadow: 0 16px 40px rgba(168, 85, 247, 0.12) !important; }

.vs-header { display: flex !important; align-items: center !important; justify-content: space-between !important; }

.vs-logo-name { font-size: 1.8rem; font-weight: 700; color: #334155; }
.vs-logo-tag { color: var(--dz-text-light); font-size: 0.9rem; margin-top: 4px; }
.vs-title { font-size: 2rem; font-weight: 700; margin-bottom: 1.5rem; color: #334155; }
.vs-label { background: rgba(192, 132, 252, 0.15); color: var(--dz-primary); padding: 5px 16px; border-radius: 999px; font-weight: 600; font-size: 0.75rem; letter-spacing: 0.05em; display: inline-block; margin-bottom: 0.8rem; }
.vs-insight-title { color: var(--dz-primary); font-size: 1.2rem; font-weight: 700; margin-bottom: 0.6rem; }

.vs-bio-number { font-size: 5rem; font-weight: 700; background: var(--dz-primary-grad); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.vs-metric-val { font-size: 2.5rem; font-weight: 800; background: var(--dz-primary-grad); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

.stTabs [data-baseweb="tab-list"] {
    background: var(--dz-surface) !important;
    backdrop-filter: blur(16px) !important;
    border-radius: 999px !important;
    border: 1px solid var(--dz-border) !important;
    padding: 0.4rem !important; gap: 0.3rem !important;
    box-shadow: var(--dz-shadow) !important;
    display: flex !important; width: 100% !important; overflow-x: hidden !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: var(--dz-text-light) !important;
    border-radius: 999px !important; padding: 0.7rem 1.5rem !important;
    font-weight: 600 !important; font-size: 0.95rem !important; border: none !important;
    flex: 1 1 0px !important; display: flex !important; justify-content: center !important; text-align: center !important; white-space: nowrap !important;
    transition: all 0.3s ease !important;
}
.stTabs [aria-selected="true"] {
    background: var(--dz-primary) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 2rem !important; }

.stNumberInput > div > div > input, .stSelectbox > div > div > div {
    background: rgba(255, 255, 255, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.9) !important;
    border-radius: 999px !important; color: var(--dz-text) !important;
    padding: 0.8rem 1.2rem !important; transition: all 0.3s ease !important;
    font-weight: 500 !important; box-shadow: inset 0 2px 5px rgba(0,0,0,0.02) !important;
}
.stNumberInput > div > div > input:focus, .stSelectbox > div > div > div:focus-within {
    box-shadow: var(--dz-glow) !important; border-color: var(--dz-primary) !important; background: #FFFFFF !important;
}
label[data-testid="stWidgetLabel"] { color: var(--dz-text) !important; font-weight: 600 !important; padding-bottom: 0.4rem !important; font-size: 0.9rem !important; }

.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--dz-primary-grad) !important; border: 3px solid #FFFFFF !important;
    box-shadow: var(--dz-shadow) !important; width: 22px !important; height: 22px !important;
}
.stSlider [data-baseweb="slider"] [data-testid="stSliderTrackActive"] { background: var(--dz-primary-grad) !important; }
.stSlider > div { color: var(--dz-text) !important; }

.stCheckbox > label { font-weight: 500 !important; color: var(--dz-text) !important; }
.stCheckbox [data-baseweb="checkbox"] > div:first-child { background: var(--dz-primary) !important; border-color: var(--dz-primary) !important; border-radius: 8px !important; }

.stButton > button {
    background: var(--dz-primary-grad) !important; color: white !important;
    border: none !important; border-radius: 999px !important;
    padding: 0.9rem 2.5rem !important; font-weight: 700 !important; font-size: 1.05rem !important;
    letter-spacing: 0.02em !important; box-shadow: 0 4px 12px rgba(6, 59, 150, 0.2) !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important; width: 100% !important;
}
.stButton > button:hover { transform: translateY(-3px) scale(1.01) !important; box-shadow: 0 6px 16px rgba(6, 59, 150, 0.3) !important; }

.vs-rec-rank {
    position: absolute; top: -12px; left: 1.5rem;
    background: var(--dz-primary-grad); color: white;
    width: 30px; height: 30px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem; font-weight: 700; box-shadow: var(--dz-glow);
}
.vs-rec-impact {
    background: rgba(136, 212, 181, 0.15); color: #0f766e;
    padding: 0.3rem 0.9rem; border-radius: 12px; font-weight: 600;
    display: inline-block; margin-bottom: 0.7rem; font-size: 0.85rem;
}
.vs-rec-plan { background: rgba(255, 255, 255, 0.5); padding: 0.7rem 1rem; border-radius: 12px; border-left: 4px solid var(--dz-primary); color: var(--dz-text); font-size: 0.85rem; }
.js-plotly-plot .plotly .bg { fill: transparent !important; }
hr { border-color: var(--dz-border) !important; }

.vs-risk-bg {
    flex: 1; height: 8px; background: rgba(168, 85, 247, 0.15);
    border-radius: 4px; overflow: hidden;
}

.diff-easy { color: #88D4B5; font-weight: 600; }
.diff-medium { color: #FFB49A; font-weight: 600; }
.diff-hard { color: #FF6B8A; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for key, default in [("analyzed", False), ("results", None), ("metrics", None), ("ai_recs", None), ("chat_history", []), ("scroll_to_top", False)]:
    if key not in st.session_state:
        st.session_state[key] = default

if st.session_state.scroll_to_top:
    components.html("""
        <script>
            const main = window.parent.document.querySelector('.main');
            if (main) main.scrollTo(0,0);
            setTimeout(() => {
                const tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
                if (tabs.length > 1) {
                    tabs[1].click();
                }
            }, 500);
        </script>
    """, height=0)
    st.session_state.scroll_to_top = False

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
# TABS
# ─────────────────────────────────────────────
if not st.session_state.analyzed:
    tabs = st.tabs(["🧬 Health Input"])
    tab1 = tabs[0]
    tab2 = tab3 = tab4 = tab5 = None
else:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧬 Health Input",
        "🔬 Biological Age",
        "📈 Future Projection",
        "🎯 Action Plan",
        "💬 AI Assistant",
    ])

# ═══════════════════════════════════
# TAB 1 — HEALTH INPUT
# ═══════════════════════════════════
with tab1:
    st.markdown('<div class="vs-label">STEP 01 · DATA COLLECTION</div>', unsafe_allow_html=True)
    st.markdown('<div class="vs-title">Enter Your Health Data</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    # ── Personal Info ──
    with col1:
        st.markdown("""
        <div class="vs-card-header">
          <div class="vs-icon-wrap icon-lilac">👤</div>
          <span class="vs-card-title">Personal Info</span>
        </div>
        <div class="vs-divider"></div>""", unsafe_allow_html=True)

        age    = st.number_input("Age (years)",    18, 100,  30)
        weight = st.number_input("Weight (kg)",    30.0, 200.0, 70.0)
        height = st.number_input("Height (cm)",    120, 220,  170)
        smoker = st.checkbox("Smoker 🚬",          value=False)
        packs  = st.slider("Packs per day", 0.0, 3.0, 0.0, 0.5) if smoker else 0.0

    # ── Vitals ──
    with col2:
        st.markdown("""
        <div class="vs-card-header">
          <div class="vs-icon-wrap icon-peach">💓</div>
          <span class="vs-card-title">Vitals</span>
        </div>
        <div class="vs-divider"></div>""", unsafe_allow_html=True)

        resting_hr = st.slider("Resting Heart Rate (bpm)", 40, 120, 72)
        systolic   = st.slider("Systolic BP (mmHg)",       90, 200, 120)
        diastolic  = st.slider("Diastolic BP (mmHg)",      60, 130, 80)
        alcohol    = st.slider("Alcohol (units/week)",      0,  50,  0)

    # ── Lifestyle ──
    with col3:
        st.markdown("""
        <div class="vs-card-header">
          <div class="vs-icon-wrap icon-mint">🏃</div>
          <span class="vs-card-title">Lifestyle</span>
        </div>
        <div class="vs-divider"></div>""", unsafe_allow_html=True)

        sleep    = st.slider("Sleep (hours/night)",   3.0, 12.0, 7.5, 0.5)
        steps    = st.slider("Daily Steps",           0, 20000,  5000, 250)
        exercise = st.slider("Exercise (min/week)",   0, 600,    150)
        stress   = st.slider("Stress Level (1–10)",   1, 10,     5)
        diet     = st.slider("Diet Quality (1–10)",   1, 10,     5)

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
        st.session_state.scroll_to_top = True
        st.rerun()

# ═══════════════════════════════════
# TAB 2 — BIOLOGICAL AGE
# ═══════════════════════════════════
if tab2 is not None:
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
if tab3 is not None:
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
if tab4 is not None:
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
                
                # --- PDF REPORT GENERATION ---
                pdf_bytes = bytes(create_pdf_report(st.session_state.metrics, st.session_state.results))
                st.download_button(
                    label="📄 Download Health Report (PDF)",
                    data=pdf_bytes,
                    file_name=f"InsightCare_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )


# ═══════════════════════════════════
# TAB 5 — AI ASSISTANT
# ═══════════════════════════════════
if tab5 is not None:
    with tab5:
        st.markdown('<div class="vs-label">24/7 SUPPORT</div>', unsafe_allow_html=True)
        st.markdown('<div class="vs-title">AI Health Assistant</div>', unsafe_allow_html=True)
        st.markdown('''
        <style>
        /* ── Chat container: scrollable area with fixed input at bottom ── */
        [data-testid="stVerticalBlock"]:has([data-testid="stChatInput"]) {
            display: flex !important;
            flex-direction: column !important;
            height: 65vh !important;
            max-height: 65vh !important;
        }
        [data-testid="stVerticalBlock"]:has([data-testid="stChatInput"]) > div:first-child {
            flex: 1 !important;
            overflow-y: auto !important;
        }

        /* ── Chat Input pinned at bottom ── */
        [data-testid="stChatInput"] {
            position: sticky !important;
            bottom: 0 !important;
            background: var(--dz-bg-grad) !important;
            padding: 12px 0 !important;
            z-index: 100 !important;
        }
        [data-testid="stChatInput"] > div {
            border-radius: 999px !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 4px 14px rgba(0,0,0,0.05) !important;
            padding: 4px 12px !important;
        }

        /* ── Hide default avatars ── */
        .stChatMessage [data-testid="chatAvatarIcon-user"],
        .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
            display: none !important;
        }

        /* ── USER message: right-aligned bubble ── */
        .stChatMessage[data-testid="stChatMessage-user"] {
            flex-direction: row-reverse !important;
            background: transparent !important;
        }
        .stChatMessage[data-testid="stChatMessage-user"] [data-testid="stChatMessageContent"] {
            background: #063B96 !important;
            color: #FFFFFF !important;
            border-radius: 20px 20px 4px 20px !important;
            padding: 12px 18px !important;
            max-width: 75% !important;
            margin-left: auto !important;
            box-shadow: 0 4px 10px rgba(6,59,150,0.15) !important;
        }
        .stChatMessage[data-testid="stChatMessage-user"] [data-testid="stChatMessageContent"] p {
            color: #FFFFFF !important;
        }

        /* ── ASSISTANT message: left-aligned bubble ── */
        .stChatMessage[data-testid="stChatMessage-assistant"] {
            background: transparent !important;
        }
        .stChatMessage[data-testid="stChatMessage-assistant"] [data-testid="stChatMessageContent"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 20px 20px 20px 4px !important;
            padding: 12px 18px !important;
            max-width: 75% !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.04) !important;
            color: #0F172A !important;
        }
        .stChatMessage[data-testid="stChatMessage-assistant"] [data-testid="stChatMessageContent"] p {
            color: #0F172A !important;
        }
        </style>
        ''', unsafe_allow_html=True)

        
        # Display existing chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # Chat input box
        if prompt := st.chat_input("Ask me about your health timeline or reports..."):
            # Add user message to history and show it
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            # Process response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    from chat_engine import generate_chat_response
                    bio = st.session_state.results["bio"]
                    metrics = st.session_state.metrics
                    ctx = {
                        "age": metrics.get("age"),
                        "biological_age": bio.get("biological_age"),
                        "cardio_risk": bio.get("cardio_risk"),
                        "metabolic_risk": bio.get("metabolic_risk"),
                        "sleep": metrics.get("sleep_hours")
                    }
                    response = generate_chat_response(st.session_state.chat_history, ctx)
                    st.markdown(response)
            
            st.session_state.chat_history.append({"role": "assistant", "content": response})
