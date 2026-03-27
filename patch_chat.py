with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

state_orig = 'for key, default in [("analyzed", False), ("results", None), ("metrics", None), ("ai_recs", None)]:'
state_new = 'for key, default in [("analyzed", False), ("results", None), ("metrics", None), ("ai_recs", None), ("chat_history", [])]:'
code = code.replace(state_orig, state_new)

tabs_orig = """if not st.session_state.analyzed:
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

tabs_new = """if not st.session_state.analyzed:
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
    ])"""
code = code.replace(tabs_orig, tabs_new)

tab5_code = """

# ═══════════════════════════════════
# TAB 5 — AI ASSISTANT
# ═══════════════════════════════════
if tab5 is not None:
    with tab5:
        st.markdown('<div class="vs-label">24/7 SUPPORT</div>', unsafe_allow_html=True)
        st.markdown('<div class="vs-title">AI Health Assistant</div>', unsafe_allow_html=True)
        
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
"""

code += tab5_code

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
