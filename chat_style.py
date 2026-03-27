with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        st.markdown('<div class="vs-title">AI Health Assistant</div>', unsafe_allow_html=True)"""

css = """
        st.markdown('''
        <style>
        /* Chat Input Styling */
        div[data-testid="stChatInput"] { padding-bottom: 20px; }
        div[data-testid="stChatInput"] > div {
            border-radius: 999px !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 4px 14px rgba(0,0,0,0.05) !important;
            padding: 8px 12px !important;
        }

        /* Hide generic avatars for a clean SMS style */
        div[data-testid="chatAvatarIcon-user"] { display: none !important; }
        div[data-testid="chatAvatarIcon-assistant"] { display: none !important; }
        
        /* User Bubble Alignment (Right) */
        div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            flex-direction: row-reverse;
            justify-content: flex-start;
        }
        div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
            background-color: #F8FAFC !important;
            border-radius: 20px 20px 4px 20px !important;
            padding: 12px 18px !important;
            border: 1px solid #E2E8F0 !important;
            color: #0F172A !important;
        }
        div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown p { color: #0F172A !important; }

        /* Bot Bubble Alignment (Left) */
        div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
            flex-direction: row;
        }
        div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 20px 20px 20px 4px !important;
            padding: 12px 18px !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03) !important;
            color: #0F172A !important;
        }
        div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown p { color: #0F172A !important; }
        
        /* Override default full width of message content */
        div[data-testid="stChatMessageContent"] {
            flex: 0 1 auto !important;
            max-width: 80% !important;
        }
        </style>
        ''', unsafe_allow_html=True)
"""

if target in text:
    text = text.replace(target, target + css)
    print("Injected CSS successfully.")
else:
    print("Target not found.")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)
