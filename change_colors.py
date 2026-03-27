import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

root_target = r':root \{[\s\S]*?\}'
root_replacement = ''':root {
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
}'''
code = re.sub(root_target, root_replacement, code, count=1)

tab_target = r'\.stTabs \[aria-selected="true"\] \{[\s\S]*?\}'
tab_replacement = '''.stTabs [aria-selected="true"] {
    background: var(--dz-primary) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04) !important;
}'''
code = re.sub(tab_target, tab_replacement, code, count=1)

code = code.replace(
    'background: radial-gradient(circle, rgba(192, 132, 252, 0.15) 0%, transparent 70%);',
    'background: transparent;'
).replace(
    'background: radial-gradient(circle, rgba(129, 140, 248, 0.15) 0%, transparent 70%);',
    'background: transparent;'
)

code = code.replace(
    'box-shadow: 0 8px 25px rgba(244, 114, 182, 0.35) !important;',
    'box-shadow: 0 4px 12px rgba(6, 59, 150, 0.2) !important;'
).replace(
    'box-shadow: 0 12px 35px rgba(244, 114, 182, 0.5) !important;',
    'box-shadow: 0 6px 16px rgba(6, 59, 150, 0.3) !important;'
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
