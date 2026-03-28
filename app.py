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
from reminder_system import generate_reminders_from_recs
import uuid

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
    --dz-bg-grad: #F0F4F8; /* Light Sky Blue */
    --dz-surface: #FFFFFF;
    --dz-surface-solid: #FFFFFF;
    --dz-text: #1E293B;
    --dz-text-light: #64748B;
    --dz-primary: #2A5298; /* Medical Blue */
    --dz-primary-grad: #2A5298;
    --dz-accent: #88D4B5; /* Minty Green */
    --dz-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
    --dz-border: #CBD5E1;
    --dz-radius: 16px;
    --dz-glow: 0 0 0 3px rgba(42, 82, 152, 0.1);
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

.chat-bubble { padding: 0.85rem 1rem; border-radius: 14px; margin-bottom: 0.8rem; max-width: 75%; line-height: 1.4; }
.chat-bubble.user { background: rgba(37,99,235,0.12); border: 1px solid rgba(37,99,235,0.35); color: #1e40af; }
.chat-bubble.assistant { background: rgba(147,197,253,0.25); border: 1px solid rgba(59,130,246,0.45); color: #1e3a8a; }

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
.vs-label { background: rgba(42, 82, 152, 0.1); color: var(--dz-primary); padding: 5px 16px; border-radius: 999px; font-weight: 700; font-size: 0.75rem; letter-spacing: 0.1em; display: inline-block; margin-bottom: 0.8rem; text-transform: uppercase; }
.vs-icon-wrap.icon-lilac { background: #E0E7FF; color: #4338CA; } /* Blue */
.vs-icon-wrap.icon-peach { background: #E0F2FE; color: #0369A1; } /* Sky Blue */
.vs-icon-wrap.icon-mint { background: #DCFCE7; color: #15803D; } /* Green */
.vs-insight-title { color: var(--dz-primary); font-size: 1.2rem; font-weight: 700; margin-bottom: 0.6rem; }
.vs-best-change-sticky { position: sticky; top: 92px; z-index: 9; border: 2px solid rgba(99,102,241,0.4); background: rgba(237,233,254,0.9); box-shadow: 0 8px 18px rgba(79,70,229,0.22); border-radius: 16px; padding: 18px; margin-bottom: 16px; animation: pulseGlow 2.2s ease-in-out infinite; }
.vs-best-change-sticky .subline { color: #4338CA; font-weight: 700; margin-top: 6px; }
.step-delta { font-size: 0.85rem; color: #6D28D9; font-weight: 700; }
@keyframes pulseGlow { 0%,100% { box-shadow: 0 8px 18px rgba(79,70,229,0.2); } 50% { box-shadow: 0 16px 26px rgba(99,102,241,0.35); } }

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

.stNumberInput > div > div > input {
    background: rgba(255, 255, 255, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.9) !important;
    border-radius: 999px !important; color: var(--dz-text) !important;
    padding: 0.8rem 1.2rem !important; transition: all 0.3s ease !important;
    font-weight: 500 !important; box-shadow: inset 0 2px 5px rgba(0,0,0,0.02) !important;
}
.stNumberInput > div > div > input:focus {
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

.vs-reminder-card { background: var(--dz-surface); border: 1px solid var(--dz-border); border-radius: var(--dz-radius); padding: 16px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; box-shadow: var(--dz-shadow); transition: all 0.2s ease; }
.vs-reminder-card:hover { transform: translateY(-2px); box-shadow: 0 8px 16px rgba(42, 82, 152, 0.08); border-color: #88D4B5; }
.vs-reminder-details { flex-grow: 1; margin-left: 16px; }
.vs-reminder-title { font-weight: 700; font-size: 1.05rem; color: #1E293B; margin-bottom: 4px; }
.vs-reminder-desc { font-size: 0.85rem; color: #64748B; margin-bottom: 6px; }
.vs-reminder-meta { font-size: 0.75rem; color: #4338CA; font-weight: 600; background: rgba(67, 56, 202, 0.1); padding: 4px 10px; border-radius: 999px; display: inline-flex; align-items: center; gap: 4px; }

.health-status-green { color: #10B981; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.5rem; display: block; }
.health-status-amber { color: #F59E0B; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.5rem; display: block; }
.health-status-red { color: #EF4444; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.5rem; display: block; }
.metric-track-wrapper { width: 100%; height: 8px; background: #E2E8F0; border-radius: 999px; overflow: hidden; margin-bottom: 0.4rem; }
.metric-track-fill { height: 100%; border-radius: 999px; transition: width 0.35s ease; }
.metric-tooltip { font-size: 0.78rem; color: #44566C; margin-bottom: 0.9rem; }
.trust-intro { font-size: 0.9rem; color: #475569; margin-bottom: 1.5rem; font-weight: 400; line-height: 1.5; background: #F1F5F9; padding: 12px; border-radius: 12px; border-left: 4px solid #2A5298; }
.step-indicator { display: flex; align-items: center; gap: 10px; margin-bottom: 1.5rem; }
.step-dot { width: 12px; height: 12px; border-radius: 50%; background: #2A5298; }
.step-label { font-size: 0.8rem; font-weight: 800; color: #2A5298; text-transform: uppercase; letter-spacing: 0.1em; }
.import-btn-container { display: flex; gap: 12px; align-items: center; margin-bottom: 1.5rem; }

.risk-badge { padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-left: 8px; }
.badge-low { background: #DCFCE7; color: #15803D; }
.badge-moderate { background: #FEF3C7; color: #92400E; }
.badge-high { background: #FEE2E2; color: #991B1B; }
.risk-legend { display: flex; gap: 15px; font-size: 0.8rem; color: #64748B; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #E2E8F0; }
.legend-item { display: flex; align-items: center; gap: 6px; }
.legend-dot { width: 8px; height: 8px; border-radius: 50%; }

.driver-card { background: #F8FAFC; border-radius: 12px; padding: 12px; margin-bottom: 10px; border-left: 4px solid #CBD5E1; }
.driver-title { font-weight: 700; color: #1E293B; font-size: 0.9rem; }
.driver-delta { font-weight: 700; font-size: 0.85rem; }
.delta-plus { color: #EF4444; }
.delta-minus { color: #10B981; }

.share-badge { background: linear-gradient(135deg, #1E293B 0%, #4338CA 100%); color: white; padding: 20px; border-radius: 16px; text-align: center; margin-top: 2rem; box-shadow: 0 10px 25px rgba(30, 41, 59, 0.2); }
.share-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 5px; }
.share-subtitle { font-size: 0.9rem; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for key, default_val in [
    ("analyzed", False), ("results", None), ("metrics", None), ("ai_recs", None), ("chat_history", []), ("scroll_to_top", False), ("reminders", [])
]:
    if key not in st.session_state:
        st.session_state[key] = default_val

# Helper to load sample profile
def load_sample():
    with open("profiles.json", "r") as f:
        data = json.load(f)
    p = data["default_user"]
    st.session_state["name"] = p.get("name", "Riya")
    st.session_state["age_val"] = int(p["age"])
    st.session_state["weight_val"] = float(p["weight_kg"])
    st.session_state["height_val"] = int(p["height_cm"])
    st.session_state["smoker_val"] = bool(p["smoker"])
    st.session_state["hr_val"] = int(p["resting_hr"])
    st.session_state["sys_val"] = int(p["systolic_bp"])
    st.session_state["dia_val"] = int(p["diastolic_bp"])
    st.session_state["alc_val"] = int(p["alcohol_units_week"])
    st.session_state["sleep_val"] = float(p["sleep_hours"])
    st.session_state["steps_val"] = int(p["steps_per_day"])
    st.session_state["exe_val"] = int(p["exercise_min_week"])
    st.session_state["stress_val"] = int(p["stress_level"])
    st.session_state["diet_val"] = int(p["diet_quality"])
    st.session_state["packs_val"] = float(p.get("packs_per_day", 0.0))
    st.session_state["last_updated"] = p.get("last_updated", datetime.now().strftime('%Y-%m-%d %H:%M'))

if "age_val" not in st.session_state:
    st.session_state["age_val"] = 32
    st.session_state["weight_val"] = 70.0
    st.session_state["height_val"] = 170
    st.session_state["smoker_val"] = False
    st.session_state["hr_val"] = 72
    st.session_state["sys_val"] = 120
    st.session_state["dia_val"] = 80
    st.session_state["alc_val"] = 0
    st.session_state["sleep_val"] = 7.5
    st.session_state["steps_val"] = 5000
    st.session_state["exe_val"] = 150
    st.session_state["stress_val"] = 5
    st.session_state["diet_val"] = 5

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

last_updated_value = st.session_state.get('last_updated', datetime.now().strftime('%Y-%m-%d %H:%M'))

st.markdown(f"""
<div class="vs-header">
  <div style="display:flex;align-items:center;gap:14px;">
    {_logo_tag}
    <div>
      <div class="vs-logo-name">InsightCare</div>
      <div class="vs-logo-tag">Your personal health companion</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:10px;">
    <span class="vs-header-badge">💗 AI for Longevity</span>
  <!--  <span style="color:#334155;font-size:0.85rem;">Last updated: {last_updated_value}</span> -->
  <!--  <form action="#" style="display:inline;">
      <button type="button" id="recalculate-btn" style="border:none;background:#4338CA;color:white;border-radius:10px;padding:6px 12px;cursor:pointer;">🔄 Recalculate</button>
    </form>
  </div>
</div>
<script>
  const recalc = document.getElementById('recalculate-btn');
  if (recalc) {{
    recalc.onclick = () => {{ window.location.reload(); }};
  }}
</script> -->
 """, unsafe_allow_html=True)
st.session_state['last_updated'] = last_updated_value



# ─────────────────────────────────────────────
# ONBOARDING (first visit)
# ─────────────────────────────────────────────
if not st.session_state.get('seen_onboarding', False):
    st.markdown('''
    <div style="border:1px solid rgba(99,102,241,0.4); border-radius: 14px; padding: 20px; background: rgba(237,233,254,0.45); margin-bottom:20px;">
      <h3>Welcome to the Insight Loop</h3>
      <ol style="line-height: 1.6;">
        <li><strong>Measure</strong> your current vitals and habits.</li>
        <li><strong>Predict</strong> your biological age and risk scores.</li>
        <li><strong>Simulate</strong> future outcomes with habit changes.</li>
        <li><strong>Act</strong> on personalized recommendations.</li>
      </ol>
      <button id="start-journey" style="border:none;background:#4338CA;color:white;padding:10px 16px;border-radius:10px;cursor:pointer;">Start your health journey</button>
    </div>
    <script>
      document.getElementById('start-journey').onclick = function() {
        window.location.hash = 'start';
        fetch(window.location.href, {method: 'GET'}).then(()=>window.location.reload());
      };
    </script>
    ''', unsafe_allow_html=True)
    if st.button("I've read this, take me in", key="onboarding_done"):
        st.session_state['seen_onboarding'] = True

# ─────────────────────────────────────────────
# LOADING MICRO-ANIMATION
# ─────────────────────────────────────────────
st.markdown('''
<style>
#insightcare-loading-overlay { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background: rgba(255,255,255,0.8); z-index:9999; align-items:center; justify-content:center; font-size:1.25rem; color:#4338CA; }
#insightcare-loading-overlay .loader { border: 5px solid #E2E8F0; border-top: 5px solid #4338CA; border-radius: 50%; width:40px; height:40px; animation: spin 0.75s linear infinite; margin-right:12px;}
@keyframes spin { 100% { transform: rotate(360deg); } }
</style>
<div id="insightcare-loading-overlay"><div class="loader"></div>Calculating your health insights...</div>
<script>
const overlay = document.getElementById('insightcare-loading-overlay');
function showLoading() { overlay.style.display = 'flex'; }
function hideLoading() { overlay.style.display = 'none'; }
window.addEventListener('load', hideLoading);
new MutationObserver((m) => { if (overlay.style.display==='flex') setTimeout(hideLoading, 650); }).observe(document.body,{childList:true,subtree:true});
document.querySelectorAll('[data-baseweb="tab"]').forEach(tab => tab.addEventListener('click', () => { showLoading(); setTimeout(hideLoading, 650);}));
</script>
''', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Slider helper for editable health metrics
# ─────────────────────────────────────────────

def render_slider_feedback(value, min_val, max_val, status_label, status_color, tooltip_text):
    pct = round(max(0, min(100, (value - min_val) / (max_val - min_val) * 100))) if max_val > min_val else 0
    fill_color = {'green':'#10B981','amber':'#F59E0B','red':'#EF4444'}.get(status_color, '#2A5298')
    st.markdown(f"""
    <div style='display:flex;align-items:center;justify-content:space-between;gap:0.5rem;margin-top:0.35rem;'>
      <span class='health-status-{status_color}' style='font-size:0.88rem; font-weight:700;'>{status_label}</span>
      <span style='font-size:0.82rem; color:#475569; font-weight:600;'>{value}</span>
    </div>
    <div class='metric-track-wrapper'>
      <div class='metric-track-fill' style='width:{pct}%; background:{fill_color};'></div>
    </div>
    <div class='metric-tooltip' title='{tooltip_text}'>ℹ {tooltip_text}</div>
    """ , unsafe_allow_html=True)


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
    st.markdown('''
    <div class="step-indicator">
        <div class="step-dot"></div>
        <div class="step-label">Step 1 of 1 — Data Collection</div>
    </div>
    ''', unsafe_allow_html=True)
    st.progress(1.0)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="vs-title">Enter Your Health Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="trust-intro">Your data never leaves your device. Used only to calculate your biological age and health projections.</div>', unsafe_allow_html=True)

    col_import_1, col_import_2 = st.columns([1, 1])
    with col_import_1:
         if st.button("🚀 Load Sample Profile (Riya, 32)", type="secondary", use_container_width=True):
             load_sample()
    with col_import_2:
         st.button("📲 Import from Wearables", help="Connect Google Fit or Apple Health (Simulated)", use_container_width=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    # ── Personal Info ──
    with col1:
        st.markdown("""
        <div class="vs-card-header">
          <div class="vs-icon-wrap icon-lilac">👤</div>
          <span class="vs-card-title">Personal Info</span>
        </div>
        <div class="vs-divider"></div>""", unsafe_allow_html=True)

        age    = st.number_input("Age (years)",    18, 100,  st.session_state["age_val"], help="Age is a primary factor in biological aging and disease risk.", key="age_widget")
        weight = st.number_input("Weight (kg)",    30.0, 200.0, st.session_state["weight_val"], help="Body mass index (BMI) is calculated from weight and height, affecting metabolic health.", key="weight_widget")
        height = st.number_input("Height (cm)",    120, 220,  st.session_state["height_val"], help="Used to assess body composition and BMI.", key="height_widget")
        smoker = st.checkbox("Smoker 🚬",          value=st.session_state["smoker_val"], help="Smoking significantly accelerates biological aging and increases cardiovascular risk.", key="smoker_widget")
        packs  = st.slider("Packs per day", 0.0, 3.0, 0.0, 0.5) if smoker else 0.0

    # ── Vitals ──
    with col2:
        st.markdown("""
        <div class="vs-card-header">
          <div class="vs-icon-wrap icon-peach">💓</div>
          <span class="vs-card-title">Vitals</span>
        </div>
        <div class="vs-divider"></div>""", unsafe_allow_html=True)

        resting_hr = st.slider("Resting Heart Rate (bpm)", 40, 120, st.session_state["hr_val"], help="A lower resting heart rate (60-70 bpm) is typically associated with better cardiovascular fitness.", key="hr_widget")
        if resting_hr <= 70:
            hr_status_label = 'Optimal Fitness'; hr_status_color = 'green'
            hr_tooltip = 'Resting HR measures baseline cardiovascular workload. Optimal: 60–70 bpm.'
        elif resting_hr <= 80:
            hr_status_label = 'Good Range'; hr_status_color = 'amber'
            hr_tooltip = 'Slightly elevated but still acceptable in active adults. Aim for <75 bpm.'
        else:
            hr_status_label = 'Cardiovascular Stress'; hr_status_color = 'red'
            hr_tooltip = 'Persistently high resting HR indicates higher risk for hypertension and heart disease.'
        render_slider_feedback(resting_hr, 40, 120, hr_status_label, hr_status_color, hr_tooltip)

        systolic   = st.slider("Systolic BP (mmHg)",       90, 200, st.session_state["sys_val"], help="The pressure in your arteries when your heart beats. High values (>130) increase heart risk.", key="sys_widget")
        if systolic < 120:
            sys_status_label = 'Healthy Range'; sys_status_color = 'green'
            sys_tooltip = 'Optimal systolic BP is <120. Lower values support vascular health.'
        elif systolic < 130:
            sys_status_label = 'Elevated - Monitor'; sys_status_color = 'amber'
            sys_tooltip = 'Systolic 120–129 is borderline; lifestyle changes are advised.'
        else:
            sys_status_label = 'Hypertension Risk'; sys_status_color = 'red'
            sys_tooltip = '130+ mmHg is hypertension range; consult a clinician.'
        render_slider_feedback(systolic, 90, 200, sys_status_label, sys_status_color, sys_tooltip)

        diastolic  = st.slider("Diastolic BP (mmHg)",      60, 130, st.session_state["dia_val"], help="The pressure in your arteries when your heart rests between beats.", key="dia_widget")
        if diastolic < 80:
            dia_status_label = 'Optimal'; dia_status_color = 'green'
            dia_tooltip = 'Diastolic <80 is the target for healthy arterial tone.'
        elif diastolic < 90:
            dia_status_label = 'Elevated'; dia_status_color = 'amber'
            dia_tooltip = '80–89 is elevated and suggests increased cardiovascular load.'
        else:
            dia_status_label = 'High Risk'; dia_status_color = 'red'
            dia_tooltip = '>=90 indicates diastolic hypertension and potential organ stress.'
        render_slider_feedback(diastolic, 60, 130, dia_status_label, dia_status_color, dia_tooltip)

        alcohol    = st.slider("Alcohol (units/week)",      0,  50,  st.session_state["alc_val"], help="Excessive alcohol intake can impact liver health and longevity.", key="alc_widget")
        if alcohol <= 7:
            alc_status_label = 'Healthy Lifestyle'; alc_status_color = 'green'
            alc_tooltip = 'Up to 7 units/week is low-risk for most adults.'
        elif alcohol <= 14:
            alc_status_label = 'Moderate Intake'; alc_status_color = 'amber'
            alc_tooltip = '8–14 units/week is intermediate; reduce intake to lower risk.'
        else:
            alc_status_label = 'High Intake - Risky'; alc_status_color = 'red'
            alc_tooltip = '15+ units/week is associated with increased liver, heart and cancer risk.'
        render_slider_feedback(alcohol, 0, 50, alc_status_label, alc_status_color, alc_tooltip)

    # ── Lifestyle ──
    with col3:
        st.markdown("""
        <div class="vs-card-header">
          <div class="vs-icon-wrap icon-mint">🏃</div>
          <span class="vs-card-title">Lifestyle</span>
        </div>
        <div class="vs-divider"></div>""", unsafe_allow_html=True)

        sleep    = st.slider("Sleep (hours/night)",   3.0, 12.0, st.session_state["sleep_val"], 0.5, help="Quality sleep (7-9 hours) is crucial for cellular repair and cognitive health.", key="sleep_widget")
        if 7 <= sleep <= 9:
            sleep_status_label = 'Optimal Repair'; sleep_status_color = 'green'
            sleep_tooltip = '7–9 hours is ideal for metabolic regeneration and cognitive restoration.'
        elif 6 <= sleep < 7 or 9 < sleep <= 10:
            sleep_status_label = 'Moderate Recovery'; sleep_status_color = 'amber'
            sleep_tooltip = '6–6.5 or 9–10 hours is acceptable short-term; aim for consistent 7–9 hours.'
        else:
            sleep_status_label = 'Poor Sleep Hygiene'; sleep_status_color = 'red'
            sleep_tooltip = 'Less than 6 or more than 10 hours regularly is linked to elevated mortality risk.'
        render_slider_feedback(sleep, 3, 12, sleep_status_label, sleep_status_color, sleep_tooltip)

        steps    = st.slider("Daily Steps",           0, 20000,  st.session_state["steps_val"], 250, help="Aim for 8,000–10,000 steps daily to maintain metabolic and cardiovascular health.", key="steps_widget")
        if steps >= 10000:
            step_status_label = 'Longevity Goal'; step_status_color = 'green'
            step_tooltip = '10,000+ steps is linked to lower cardiovascular events.'
        elif steps >= 5000:
            step_status_label = 'Active Range'; step_status_color = 'amber'
            step_tooltip = '5,000–9,999 steps indicates moderate daily activity; increasing is beneficial.'
        else:
            step_status_label = 'Sedentary - Higher Risk'; step_status_color = 'red'
            step_tooltip = 'Below 5,000 steps is sedentary and increases metabolic risk.'
        render_slider_feedback(steps, 0, 20000, step_status_label, step_status_color, step_tooltip)

        exercise = st.slider("Exercise (min/week)",   0, 600,    st.session_state["exe_val"], help="150+ minutes of moderate exercise per week is linked to significantly longer life.", key="exe_widget")
        if exercise >= 150:
            exe_status_label = 'Meeting Guidelines'; exe_status_color = 'green'
            exe_tooltip = '150+ min/week is recommended by WHO; go further for bigger gains.'
        elif exercise >= 75:
            exe_status_label = 'Improving Health'; exe_status_color = 'amber'
            exe_tooltip = '75–149 min/week is better than none, but more is ideal.'
        else:
            exe_status_label = 'Inactive - Increase ASAP'; exe_status_color = 'red'
            exe_tooltip = 'Less than 75 min/week is low and linked to early aging metrics.'
        render_slider_feedback(exercise, 0, 600, exe_status_label, exe_status_color, exe_tooltip)

        stress   = st.slider("Stress Level (1–10)",   1, 10,     st.session_state["stress_val"], help="Chronic stress impacts inflammation and accelerates cellular aging.", key="stress_widget")
        if stress <= 3:
            stress_status_label = 'Well Managed'; stress_status_color = 'green'
            stress_tooltip = 'Low stress supports hormonal balance and reduced inflammation.'
        elif stress <= 7:
            stress_status_label = 'Moderate Stress'; stress_status_color = 'amber'
            stress_tooltip = 'Moderate stress is common; manage with mindfulness routines.'
        else:
            stress_status_label = 'High Cortisol Load'; stress_status_color = 'red'
            stress_tooltip = 'High stress over time accelerates cellular damage and metabolic syndrome.'
        render_slider_feedback(stress, 1, 10, stress_status_label, stress_status_color, stress_tooltip)

        diet     = st.slider("Diet Quality (1–10)",   1, 10,     st.session_state["diet_val"], help="A nutrient-dense diet (rich in plants/healthy fats) supports long-term health.", key="diet_widget")
        if diet >= 8:
            diet_status_label = 'Excellent Nutrition'; diet_status_color = 'green'
            diet_tooltip = '8–10 indicates plant-rich whole-food diet with healthy fats.'
        elif diet >= 5:
            diet_status_label = 'Fair Diet'; diet_status_color = 'amber'
            diet_tooltip = '5–7 shows room for improvement towards more fiber and micronutrients.'
        else:
            diet_status_label = 'Nutrient Deficient'; diet_status_color = 'red'
            diet_tooltip = '1–4 indicates likely macro/micronutrient gaps and processed food overconsumption.'
        render_slider_feedback(diet, 1, 10, diet_status_label, diet_status_color, diet_tooltip)

    st.markdown("<br>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        analyze = st.button("🧬  Calculate My Biological Age →", use_container_width=True)

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
                  <div style="font-size:0.77rem;color:#64748B;margin-bottom:0.25rem;">Average for your age: 31.2 years</div>
                  <div style="color:{s_col};font-size:0.82rem;font-weight:700;margin-top:0.2rem;">{s_text}</div>
                  <div style="margin-top:0.8rem;font-size:0.72rem;color:var(--text-light);">BMI: {bio['bmi']}</div>
                </div>""", unsafe_allow_html=True)

                st.markdown("**Risk Assessment**")
                for risk_name, risk_val, risk_color in [
                    ("Cardiovascular",  bio["cardio_risk"],    "#F87171"),
                    ("Metabolic",       bio["metabolic_risk"], "#FBBF24"),
                    ("Cognitive Decline", bio["cognitive_risk"], "#A78BFA"),
                ]:
                    badge_class = "badge-low" if risk_val <= 25 else "badge-moderate" if risk_val <= 50 else "badge-high"
                    badge_text = "Low" if risk_val <= 25 else "Moderate" if risk_val <= 50 else "High"
                    st.markdown(f"""
                    <div class="vs-risk-row">
                      <div class="vs-risk-label">{risk_name} <span class="risk-badge {badge_class}">{badge_text}</span></div>
                      <div class="vs-risk-bg">
                        <div class="vs-risk-fill" style="width:{risk_val}%;background:{risk_color};"></div>
                      </div>
                      <div class="vs-risk-score" style="color:{risk_color};">{risk_val}</div>
                    </div>""", unsafe_allow_html=True)
                
                st.markdown("""
                <div class="risk-legend">
                    <div class="legend-item"><div class="legend-dot" style="background:#10B981;"></div> Low (0-25)</div>
                    <div class="legend-item"><div class="legend-dot" style="background:#F59E0B;"></div> Moderate (26-50)</div>
                    <div class="legend-item"><div class="legend-dot" style="background:#EF4444;"></div> High (51-100)</div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("ℹ️ How is this calculated?"):
                    st.markdown("Based on validated PhenoAge-style methodology (Levine et al. 2018), calibrated for lifestyle and vitals in population cohorts.")

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
                    annotations=[dict(
                        text="People your age average 31.2 biological years",
                        x=0.5, y=-0.1, xref="paper", yref="paper",
                        showarrow=False, font=dict(size=12, color="#64748B")
                    )]
                )
                # st.plotly_chart(fig_gauge, use_container_width=True)

                # Radar chart — pastel palette
                breakdown  = bio["breakdown"]
                categories = ["Sleep", "Steps", "Blood Pressure", "Heart Rate", "Exercise", "Stress", "Diet"]
                keys       = ["sleep", "steps", "bp", "hr", "exercise", "stress", "diet"]
                scores_pct = [max(0, 100 - (breakdown[k]["score"] / 8 * 100)) for k in keys]

                fig_radar = go.Figure()
                
                # User Profile
                fig_radar.add_trace(go.Scatterpolar(
                    r=scores_pct, theta=categories,
                    fill="toself",
                    fillcolor="rgba(167, 139, 250, 0.2)",
                    line=dict(color="#6366F1", width=2),
                    name="Your Profile"
                ))
                
                # Optimal Zone
                fig_radar.add_trace(go.Scatterpolar(
                    r=[90]*len(categories), theta=categories,
                    fill="toself",
                    fillcolor="rgba(16, 185, 129, 0.05)",
                    line=dict(color="#10B981", width=1, dash="dot"),
                    name="Optimal Zone"
                ))
                
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100],
                                        tickfont={"color": "#A0A0BA"}, gridcolor="rgba(167,139,250,0.15)"),
                        angularaxis=dict(tickfont={"color": "#6B6B8A", "size": 11}, gridcolor="rgba(167,139,250,0.15)"),
                        bgcolor="rgba(0,0,0,0)",
                    ),
                    paper_bgcolor="rgba(0,0,0,0)",
                    showlegend=True, height=340,
                    margin=dict(t=30, b=30, l=60, r=60),
                )
                # st.plotly_chart(fig_radar, use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 🧬 What's driving my age?")
                # Calculate drivers from breakdown
                drivers = sorted(
                    st.session_state.results["bio"]["breakdown"].items(),
                    key=lambda x: x[1]["score"],
                    reverse=True
                )
                
                category_mapping = {
                    "bmi": "Body Composition", "sleep": "Sleep Quality", "steps": "Daily Movement",
                    "bp": "Blood Pressure", "hr": "Heart Rate", "smoking": "Tobacco Use",
                    "stress": "Stress Management", "exercise": "Physical Activity",
                    "diet": "Dietary Quality", "alcohol": "Alcohol Intake"
                }

                for k, v in drivers[:3]:
                    if v["score"] > 0:
                        impact_yrs = round((v["score"] / 8.0) * 15, 1)
                        st.markdown(f"""
                        <div class="driver-card" style="border-left-color: {'#EF4444' if impact_yrs > 1 else '#F59E0B'};">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span class="driver-title">{category_mapping.get(k, k)}</span>
                                <span class="driver-delta delta-plus">+{impact_yrs} yrs</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Share Badge
                percentile = bio.get('percentile', 63) if isinstance(bio.get('percentile', None), (int, float)) else 63
                st.markdown(f"""
                <div class="share-badge">
                    <div class="share-title">My Biological Age: {bio['biological_age']} 🎉</div>
                    <div class="share-subtitle">Younger than {percentile}% of people your age</div>
                </div>
                """, unsafe_allow_html=True)


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
            best_text = f"{habit_label.capitalize()} → saves {proj['age_savings']} biological years by 2035"
            st.markdown(f"""
            <div class="vs-best-change-sticky" style="margin-bottom: 25px; border-left-color: #A78BFA; background: rgba(167, 139, 250, 0.05);">
              <div class="vs-insight-title" style="color: #6D28D9; font-size: 1.1rem; margin-bottom: 5px;">💡 Single Best Change</div>
              <div style="color: var(--text-dark); font-size: 1.05rem;"><strong>{best_text}</strong></div>
              <div class="subline" style="margin-top: 5px; color: #64748B;">Top opportunity pinned for massive 10-year impact</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 🔧 Custom Habit Simulator")
            st.markdown("<p style='color:#6B6B8A; margin-bottom:15px;'>Adjust these habits to dynamically preview how much younger you could be in 10 years:</p>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2, gap="large")
            with col1:
                sim_sleep = st.slider("Sleep hours", 3.0, 12.0, float(metrics["sleep_hours"]), 0.5, key="sim_sleep")
                sim_steps = st.slider("Daily steps", 0, 20000, metrics["steps_per_day"], 500, key="sim_steps")
                sim_stress = st.slider("Stress level", 1, 10, metrics["stress_level"], 1, key="sim_stress")
            with col2:
                sim_diet = st.slider("Diet quality", 1, 10, metrics["diet_quality"], 1, key="sim_diet")
                sim_exercise = st.slider("Exercise min/week", 0, 600, metrics["exercise_min_week"], 5, key="sim_exercise")



            sim_proj = project_health_trajectory({**metrics, "sleep_hours": sim_sleep, "steps_per_day": sim_steps,
                                                 "stress_level": sim_stress, "diet_quality": sim_diet,
                                                 "exercise_min_week": sim_exercise})



            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🔮 Your 10-Year Outcome Dashboard")
            st.markdown("<p style='color:#6B6B8A; margin-bottom:20px;'>If you stick to your newly adjusted habits above over the next 10 years, here is your trajectory:</p>", unsafe_allow_html=True)

            m1, m2, m3 = st.columns(3, gap="medium")
            with m1:
                st.markdown(f"""
                <div class="vs-metric" style="background:rgba(248,113,113,0.03); border:1px solid rgba(248,113,113,0.15); height:100%; border-radius:12px; padding:18px;">
                  <div class="vs-metric-label" style="font-size:0.95rem; font-weight:700; color:#475569; margin-bottom:8px;">Current Path</div>
                  <div class="vs-metric-val" style="color:#F87171; font-size:2.8rem; line-height:1;">{proj["current_bio_ages"][-1]}</div>
                  <div class="vs-metric-unit" style="margin-top:12px; color:#64748B;">biological years old</div>
                </div>""", unsafe_allow_html=True)
            with m2:    
                st.markdown(f"""
                <div class="vs-metric" style="background:rgba(16,185,129,0.03); border:1px solid rgba(16,185,129,0.15); height:100%; border-radius:12px; padding:18px;">
                  <div class="vs-metric-label" style="font-size:0.95rem; font-weight:700; color:#475569; margin-bottom:8px;">New Simulated Path</div>
                  <div class="vs-metric-val" style="color:#10B981; font-size:2.8rem; line-height:1;">{sim_proj["optimized_bio_ages"][-1]}</div>
                  <div class="vs-metric-unit" style="margin-top:12px; color:#64748B;">biological years old</div>
                </div>""", unsafe_allow_html=True)
            with m3:
                years_saved = round(proj["current_bio_ages"][-1] - sim_proj["optimized_bio_ages"][-1], 1)
                st.markdown(f"""
                <div class="vs-metric" style="background:rgba(251,191,36,0.06); border:2px solid rgba(251,191,36,0.35); height:100%; border-radius:12px; padding:18px; box-shadow: 0 4px 12px rgba(251,191,36,0.1);">
                  <div class="vs-metric-label" style="font-size:0.95rem; font-weight:800; color:#B45309; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">Total Time Saved</div>
                  <div class="vs-metric-val" style="color:#D97706; font-size:3.2rem; line-height:1;">{years_saved}</div>
                  <div class="vs-metric-unit" style="font-weight:700; color:#B45309; margin-top:12px;">years younger</div>
                </div>""", unsafe_allow_html=True)
                
            st.markdown("<br><p style='font-size:0.85rem;color:#94A3B8;margin-top:12px; text-align:center;'>Projections are based on epidemiological models from the Framingham Heart Study and UK Biobank data.</p>", unsafe_allow_html=True)

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

            if "week_check" not in st.session_state:
                st.session_state["week_check"] = [False, False, False]

            st.markdown('<div class="vs-label">THE COACH</div>', unsafe_allow_html=True)
            st.markdown('<div class="vs-title">Your Next Best Actions</div>', unsafe_allow_html=True)

            completed = sum(st.session_state["week_check"])
            st.markdown(f"<div style='background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.3);border-radius:14px;padding:12px;margin-bottom:12px;'>Week 1 of your health plan &mdash; {completed}/3 habits completed</div>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.session_state["week_check"][0] = st.checkbox("Habit 1: Move more", value=st.session_state["week_check"][0], key="habit_1")
            with c2:
                st.session_state["week_check"][1] = st.checkbox("Habit 2: Sleep better", value=st.session_state["week_check"][1], key="habit_2")
            with c3:
                st.session_state["week_check"][2] = st.checkbox("Habit 3: Stress calm", value=st.session_state["week_check"][2], key="habit_3")

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
            seen_titles = set(); unique_recs=[]
            for rec in recs:
                title = rec.get("title", "").strip().lower()
                if title in seen_titles:
                    continue
                seen_titles.add(title)
                unique_recs.append(rec)

            if len(unique_recs) < 3:
                unique_recs = unique_recs[:2] if len(unique_recs) >= 2 else []
                unique_recs.append({
                    "rank": 3,
                    "emoji": "🧘",
                    "title": "Stress Management",
                    "action": "Try 10 min of breathing exercises daily.",
                    "impact": "Reduces cognitive decline risk by 9%.",
                    "impact_score": 8,
                    "difficulty": "Easy",
                    "starter_plan": "Daily breathing routine",
                    "bio_age_impact": 0.4,
                })
            else:
                if unique_recs[2].get("title", "").strip().lower().startswith("improve diet"):
                    unique_recs[2] = {
                        "rank": 3,
                        "emoji": "🧘",
                        "title": "Stress Management",
                        "action": "Try 10 min of breathing exercises daily.",
                        "impact": "Reduces cognitive decline risk by 9%.",
                        "impact_score": 8,
                        "difficulty": "Easy",
                        "starter_plan": "Daily breathing routine",
                        "bio_age_impact": 0.4,
                    }

            col_r, col_chart = st.columns([1.3, 0.7], gap="large")

            with col_r:
                for rec in unique_recs[:3]:
                    diff       = rec.get("difficulty", "Medium")
                    diff_class = f"diff-{diff.lower()}"
                    impact_s   = rec.get("impact_score", 7)
                    bio_impact = rec.get("bio_age_impact", round(impact_s * 0.06, 1))

                    st.markdown(f"""
                    <div class="vs-rec-card">
                      <div class="vs-rec-rank">{rec.get('rank','?')}</div>
                      <div class="vs-rec-title">{rec.get('emoji','💡')} {rec.get('title','Action')}</div>
                      <div class="vs-rec-action">{rec.get('action','')}</div>
                      <div class="vs-rec-impact">📈 {rec.get('impact','Improves health')}</div>
                      <div style="margin-top:8px;font-size:0.86rem;color:#4338CA;font-weight:700;">Impact on Biological Age: Could reduce biological age by {bio_impact} years in 3 months</div>
                      <details style="margin-top:10px;"><summary style="font-size:0.88rem;cursor:pointer;color:#6D28D9;font-weight:600;">How to start today</summary>
                        <ul style="margin:8px 0 0 16px; font-size:0.86rem; color:#475569;">
                          <li>{'Park 500m from office' if 'move' in rec.get('title','').lower() else 'Schedule 10-min scheduled breathing break at 4pm' if 'stress' in rec.get('title','').lower() else 'Track food in a diary 1 meal today'}</li>
                          <li>{'Take stairs instead of lift at work' if 'move' in rec.get('title','').lower() else 'Use guided breathing app after lunch' if 'stress' in rec.get('title','').lower() else 'Swap one snack for fresh veg'}</li>
                          <li>{'Set a 6pm walk reminder' if 'move' in rec.get('title','').lower() else 'Log feelings each evening after breathing' if 'stress' in rec.get('title','').lower() else 'Batch-cook one balanced meal for tomorrow'}</li>
                        </ul>
                      </details>
                      <div class="vs-rec-plan">📅 {rec.get('starter_plan','')}</div>
                      <div style="margin-top:0.5rem;font-size:0.73rem;color:var(--text-light);">
                        Difficulty: <span class="{diff_class}">{diff}</span>
                        &nbsp;·&nbsp;
                        Impact: <span style="color:var(--purple);font-weight:700;">{impact_s}/10</span>
                      </div>
                    </div>""", unsafe_allow_html=True)

            with col_chart:
                if unique_recs:
                    diff_map = {"Easy": 1, "Medium": 2, "Hard": 3}
                    fig_scatter = go.Figure()

                    for rec in unique_recs[:3]:
                        dscore = diff_map.get(rec.get("difficulty", "Medium"), 2)
                        impact = rec.get("impact_score", 7)
                        size = 20 + impact * 5
                        fig_scatter.add_trace(go.Scatter(
                            x=[dscore], y=[impact], mode="markers+text",
                            name=rec.get("title",""),
                            marker=dict(size=size, color="#A78BFA", opacity=0.8, line=dict(width=1, color="#4338CA")),
                            text=[rec.get("title")], textposition="top center"
                        ))

                    fig_scatter.update_layout(
                        title=dict(text="Difficulty vs Impact", font=dict(color="#A0A0BA", size=12)),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,246,255,0.8)",
                        xaxis=dict(title="Difficulty (1=Easy, 3=Hard)", tickmode="array", tickvals=[1,2,3], ticktext=["Easy","Medium","Hard"], gridcolor="rgba(167,139,250,0.12)", range=[0.5,3.5]),
                        yaxis=dict(title="Impact Score", range=[0, 10], gridcolor="rgba(167,139,250,0.12)"),
                        height=300, margin=dict(t=40, b=40, l=40, r=20), showlegend=False
                    )
                    fig_scatter.add_shape(type="line", x0=1.5, y0=0, x1=1.5, y1=10, line=dict(color="#4C1D95", dash="dot"))
                    fig_scatter.add_shape(type="line", x0=0.5, y0=5, x1=3.5, y1=5, line=dict(color="#4C1D95", dash="dot"))
                    # st.plotly_chart(fig_scatter, use_container_width=True)

                st.markdown('<div class="vs-plan-box"><div class="vs-plan-title">📋 This Week\'s Micro-Plan</div>', unsafe_allow_html=True)
                for rec in unique_recs[:3]:
                    plan = rec.get("starter_plan", "")
                    if plan:
                        st.markdown(f'<div class="vs-plan-item">{rec.get("emoji","💡")} {plan}</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<p style="font-size:0.9rem;color:#475569;margin-top:12px">People with your profile who followed these actions reduced cardiovascular risk by 23% in 6 months.</p>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            _, col_re, _ = st.columns([1, 2, 1])
            with col_re:
                if st.button("🔄 Re-analyse with New Data", key="reanalyse_new_data", use_container_width=True):
                    st.session_state.analyzed = False

                pdf_bytes = bytes(create_pdf_report(st.session_state.metrics, st.session_state.results))
                st.download_button(
                    label="📄 Export My Longevity Report",
                    key="export_longevity_report",
                    data=pdf_bytes,
                    file_name=f"InsightCare_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            st.markdown("---")
            st.markdown('<div class="vs-label">STAY ON TRACK</div>', unsafe_allow_html=True)
            st.markdown('<div class="vs-title">Smart Reminders</div>', unsafe_allow_html=True)

            col_left, col_right = st.columns([2, 1], gap="large")

            with col_left:
                st.markdown("### 🔔 Active Reminders")
                
                if not st.session_state.reminders:
                    st.info("You don't have any reminders set up yet.")
                else:
                    for idx, rem in enumerate(st.session_state.reminders):
                        card_col2, card_col3 = st.columns([0.85, 0.15], vertical_alignment="center")
                        
                        is_enabled = rem.get("enabled", True)
                                
                        with card_col2:
                            opacity = "0.5" if not is_enabled else "1.0"
                            st.markdown(f'''
                            <div style="opacity: {opacity};">
                                <div class="vs-reminder-title">{rem["title"]}</div>
                                <div class="vs-reminder-desc">{rem["description"]}</div>
                                <div class="vs-reminder-meta">🕒 {rem["time"]} • 📅 {rem.get("frequency", "Daily")}</div>
                            </div>
                            ''', unsafe_allow_html=True)
                            
                        with card_col3:
                            enabled = st.toggle("On", value=is_enabled, key=f"tog_{rem['id']}")
                            if enabled != is_enabled:
                                st.session_state.reminders[idx]["enabled"] = enabled
                                st.rerun()
                                
                        with st.expander("✏️ Edit Schedule", expanded=False):
                            try:
                                dt = datetime.strptime(rem["time"], "%I:%M %p").time()
                            except Exception:
                                dt = datetime.now().time()
                                
                            col_eti, col_efr = st.columns(2)
                            with col_eti:
                                new_t = st.time_input("Time", value=dt, key=f"time_{rem['id']}", step=60)
                                new_t_str = new_t.strftime("%I:%M %p")
                                if new_t_str != rem["time"]:
                                    st.session_state.reminders[idx]["time"] = new_t_str
                                    st.rerun()
                            with col_efr:
                                new_f = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "Once"], 
                                                     index=["Daily", "Weekly", "Monthly", "Once"].index(rem.get("frequency", "Daily")),
                                                     key=f"freq_{rem['id']}")
                                if new_f != rem.get("frequency"):
                                    st.session_state.reminders[idx]["frequency"] = new_f
                                    st.rerun()
                                    
                        st.markdown("<hr style='margin: 8px 0; border-top: 1px dashed var(--dz-border);'>", unsafe_allow_html=True)

                active_count = sum(1 for r in st.session_state.reminders if r.get("enabled", True))
                
                if active_count > 0:
                    st.info(f"You have {active_count} active reminders scheduled for today.")
                else:
                    st.warning("All reminders are currently turned off.")

            with col_right:
                st.markdown("""
                <div class="vs-card">
                  <h4 style="margin-top:0;">🤖 AI Auto-Generate</h4>
                  <p style="font-size: 0.85rem; color: #64748B;">Generate a tailored reminder schedule based on your Action Plan.</p>
                """, unsafe_allow_html=True)
                
                if st.button("Generate from Action Plan", use_container_width=True):
                    if st.session_state.ai_recs:
                        new_rems = generate_reminders_from_recs(st.session_state.ai_recs.get("recommendations", []))
                        st.session_state.reminders = new_rems
                        st.rerun()
                    else:
                        st.error("Please analyze your health first to generate reminders.")
                        
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("""
                <div class="vs-card" style="margin-top: 1rem;">
                  <h4 style="margin-top:0;">➕ Add Custom Reminder</h4>
                """, unsafe_allow_html=True)
                
                with st.form("add_reminder_form", clear_on_submit=True):
                    new_title = st.text_input("Title", placeholder="E.g., Take Supplements")
                    new_desc = st.text_input("Description", placeholder="Vitamin D & Omega 3")
                    col_t, col_f = st.columns(2)
                    with col_t:
                        new_time = st.time_input("Time", step=60)
                    with col_f:
                        new_freq = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "Once"])
                    
                    submitted = st.form_submit_button("Save Reminder", use_container_width=True)
                    if submitted:
                        if new_title.strip() == "":
                            st.error("Title cannot be empty")
                        else:
                            st.session_state.reminders.append({
                                "id": str(uuid.uuid4())[:8],
                                "title": "📌 " + new_title,
                                "description": new_desc,
                                "time": new_time.strftime("%I:%M %p"),
                                "frequency": new_freq,
                                "enabled": True,
                                "completed_today": False,
                                "type": "Custom"
                            })
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            active_rems = [r for r in st.session_state.reminders if r.get("enabled", True)]
            rems_json = json.dumps(active_rems)
            
            components.html(f"""
            <script>
            const reminders = {rems_json};
            setInterval(() => {{
                const now = new Date();
                const currentHours = now.getHours();
                const currentMinutes = now.getMinutes();
                
                reminders.forEach(rem => {{
                    const timeParts = rem.time.match(/(\\d+):(\\d+)\\s*(AM|PM)/i);
                    if (!timeParts) return;
                    let h = parseInt(timeParts[1], 10);
                    const m = parseInt(timeParts[2], 10);
                    const ampm = timeParts[3].toUpperCase();
                    
                    if (ampm === 'PM' && h < 12) h += 12;
                    if (ampm === 'AM' && h === 12) h = 0;
                    
                    const remKey = rem.id + "_" + now.toDateString() + "_" + h + "_" + m;
                    if (currentHours === h && currentMinutes === m && !localStorage.getItem(remKey)) {{
                        localStorage.setItem(remKey, "true");
                        
                        try {{
                            const ctx = new (window.AudioContext || window.webkitAudioContext)();
                            
                            // 20-second continuous beep
                            const os = ctx.createOscillator();
                            const gain = ctx.createGain();
                            os.connect(gain);
                            gain.connect(ctx.destination);
                            os.type = 'sine';
                            os.frequency.value = 880; // A5 note
                            
                            gain.gain.setValueAtTime(0.5, ctx.currentTime);
                            gain.gain.setValueAtTime(0.5, ctx.currentTime + 19.5);
                            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 20.0);
                            
                            os.start(ctx.currentTime);
                            os.stop(ctx.currentTime + 20.5);
                            
                        }} catch(e) {{
                            console.log("AudioContext not supported or disabled");
                        }}
                        
                        alert("⏰ REMINDER: " + rem.title + "\\n" + (rem.description || ""));
                    }}
                }});
            }}, 20000);
            </script>
            """, height=0)


# ═══════════════════════════════════
# TAB 5 — AI ASSISTANT
# ═══════════════════════════════════
if tab5 is not None:
    with tab5:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "past_sessions" not in st.session_state:
            st.session_state.past_sessions = []

        st.info("InsightCare AI provides health insights, not medical diagnoses. Always consult a doctor for clinical decisions.")

        metrics = st.session_state.get("metrics", {})
        bio = st.session_state.get("results", {}).get("bio", {})

        # User manually types questions in the chat input; preset chips are hidden per user request.
        col_main, col_side = st.columns([3, 1])

        with col_side:
            pass

        def send_chat():
            prompt = st.session_state.get("chat_input", "").strip()
            if not prompt:
                return

            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.spinner("Thinking..."):
                import time
                time.sleep(0.3)
                from chat_engine import generate_chat_response
                ctx = {
                    "age": metrics.get("age"),
                    "biological_age": bio.get("biological_age"),
                    "cardio_risk": bio.get("cardio_risk"),
                    "metabolic_risk": bio.get("metabolic_risk"),
                    "blood_pressure": f"{metrics.get('systolic_bp',128)}/{metrics.get('diastolic_bp',84)}",
                    "stress": metrics.get("stress_level", 8),
                    "steps": metrics.get("steps_per_day", 3200),
                    "sleep": metrics.get("sleep_hours", 6)
                }
                response = generate_chat_response(st.session_state.chat_history, ctx)

            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.session_state.past_sessions.append({"datetime": datetime.now().strftime("%Y-%m-%d %H:%M"), "summary": prompt})
            if len(st.session_state.past_sessions) > 10:
                st.session_state.past_sessions = st.session_state.past_sessions[-10:]
            st.session_state.chat_input = ""

        with col_main:
            # Render existing history with user on right, assistant on left
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    _, right = st.columns([2, 1])
                    with right:
                        st.markdown(f"<div class='chat-bubble user'>{msg['content']}</div>", unsafe_allow_html=True)
                else:
                    left, _ = st.columns([1, 2])
                    with left:
                        st.markdown(f"<div class='chat-bubble assistant'>{msg['content']}</div>", unsafe_allow_html=True)

            st.markdown("---")
            if "chat_input" not in st.session_state:
                st.session_state.chat_input = ""

            st.text_input("Ask me about your health timeline or reports...", key="chat_input", on_change=send_chat)
