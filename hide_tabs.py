import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

tabs_orig = """tab1, tab2, tab3, tab4 = st.tabs([
    "🧬 Health Input",
    "🔬 Biological Age",
    "📈 Future Projection",
    "🎯 Action Plan",
])"""

tabs_new = """if not st.session_state.analyzed:
    tabs = st.tabs(["🧬 Health Input"])
    tab1 = tabs[0]
    tab2 = tab3 = tab4 = None
else:
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧬 Health Input",
        "🔬 Biological Age",
        "📈 Future Projection",
        "🎯 Action Plan",
    ])"""

code = code.replace(tabs_orig, tabs_new)

analyze_orig = """        st.session_state.ai_recs  = ai_recs
        st.success("✅ Analysis complete! Switch to the other tabs to see your results.")"""
analyze_new = """        st.session_state.ai_recs  = ai_recs
        st.rerun()"""
code = code.replace(analyze_orig, analyze_new)

lines = code.split('\\n')
new_lines = []
in_conditional_tab = False

for line in lines:
    if line.startswith('with tab2:') or line.startswith('with tab3:') or line.startswith('with tab4:'):
        tab_var = line.split(' ')[1][:-1]
        new_lines.append(f"if {tab_var} is not None:")
        new_lines.append("    " + line)
        in_conditional_tab = True
    elif in_conditional_tab:
        if line.startswith('# ════'):
            in_conditional_tab = False
            new_lines.append(line)
        else:
            new_lines.append("    " + line if line else "")
    else:
        new_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write('\\n'.join(new_lines))
