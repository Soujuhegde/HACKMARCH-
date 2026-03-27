with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(r"if tab2 is not None:\n    with tab2:\n        if not st.session_state.analyzed:", "if tab2 is not None:\n    with tab2:\n        if not st.session_state.analyzed:\n")
text = text.replace(r"if tab3 is not None:\n    with tab3:\n        if not st.session_state.analyzed:", "if tab3 is not None:\n    with tab3:\n        if not st.session_state.analyzed:\n")
text = text.replace(r"if tab4 is not None:\n    with tab4:\n        if not st.session_state.analyzed:", "if tab4 is not None:\n    with tab4:\n        if not st.session_state.analyzed:\n")

# Just in case `if not` wasn't the exact string
text = text.replace(r"if tab2 is not None:\n    with tab2:\n", "if tab2 is not None:\n    with tab2:\n")
text = text.replace(r"if tab3 is not None:\n    with tab3:\n", "if tab3 is not None:\n    with tab3:\n")
text = text.replace(r"if tab4 is not None:\n    with tab4:\n", "if tab4 is not None:\n    with tab4:\n")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
