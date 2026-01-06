import streamlit as st
from database.auth_manager import AuthManager
from core.styles_manager import StylesManager
from core.brain_engine import BrainEngine

st.set_page_config(page_title="WORM-GPT", page_icon="💀", layout="wide")

# تطبيق التصميم
StylesManager.apply_global_css()

auth = AuthManager()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # (كود تسجيل الدخول القديم كما هو)
    st.title("🧬 WORM-GPT ACCESS")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Unlock"):
        if auth.verify_login(u, p):
            st.session_state.authenticated = True
            st.rerun()
else:
    # واجهة الشات الحقيقية
    st.title("💀 WORM-GPT NEURAL TERMINAL")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter Command..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            brain = BrainEngine()
            response = brain.get_response(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})