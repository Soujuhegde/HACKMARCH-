import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

new_css = '''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');

:root {
    --dz-bg-grad: linear-gradient(135deg, #F3E8FF 0%, #E0F2FE 50%, #FCE7F3 100%);
    --dz-surface: rgba(255, 255, 255, 0.65);
    --dz-surface-solid: #FFFFFF;
    --dz-text: #475569;
    --dz-text-light: #94A3B8;
    --dz-primary: #A855F7;
    --dz-primary-grad: linear-gradient(135deg, #C084FC, #818CF8, #F472B6);
    --dz-shadow: 0 12px 36px rgba(168, 85, 247, 0.08);
    --dz-border: rgba(255, 255, 255, 0.6);
    --dz-radius: 24px;
    --dz-glow: 0 0 20px rgba(192, 132, 252, 0.4);
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
    background: radial-gradient(circle, rgba(192, 132, 252, 0.15) 0%, transparent 70%);
    border-radius: 50%; z-index: 0; pointer-events: none;
    animation: dz-float 12s ease-in-out infinite alternate;
}
.stApp::after {
    content: ''; position: fixed; bottom: -10%; right: -15%;
    width: 65vw; height: 65vw;
    background: radial-gradient(circle, rgba(129, 140, 248, 0.15) 0%, transparent 70%);
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
    background: var(--dz-surface-solid) !important; color: var(--dz-primary) !important;
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
    letter-spacing: 0.02em !important; box-shadow: 0 8px 25px rgba(244, 114, 182, 0.35) !important;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important; width: 100% !important;
}
.stButton > button:hover { transform: translateY(-3px) scale(1.01) !important; box-shadow: 0 12px 35px rgba(244, 114, 182, 0.5) !important; }

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
</style>'''

# Regex to safely replace the entire <style> block
updated_code = re.sub(r'<style>.*?</style>', new_css, code, flags=re.DOTALL)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(updated_code)
