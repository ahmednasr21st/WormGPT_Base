import streamlit as st
import json
import os
import random
from datetime import datetime, timedelta

# --- 1. استيراد المحركات (سيتم تحميلها تدريجياً) ---
# نستخدم try/except لضمان عدم توقف الموقع إذا لم نرفع باقي الـ 22 ملفاً بعد
try:
    from core.styles_manager import StylesManager
    from core.brain_engine import BrainEngine
    from database.auth_manager import AuthManager
except ImportError:
    pass

# --- 2. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="WORM-GPT v2.0", page_icon="💀", layout="wide")

# تطبيق التصميم المظلم والنيون الأحمر
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
    .logo-text { font-size: 45px; font-weight: bold; color: #ffffff; text-align: center; letter-spacing: 2px; }
    .neon-line { height: 2px; width: 100%; background: linear-gradient(90deg, transparent, #ff0000, transparent); box-shadow: 0 0 10px #ff0000; margin-bottom: 30px; }
    .stChatMessage { border-radius: 0px !important; border-bottom: 1px solid #30363d !important; }
    [data-testid="stSidebar"] { background-color: #0d1117 !important; border-right: 1px solid #ff000033; }
    .admin-box { border: 1px solid #ff0000; padding: 20px; border-radius: 10px; background: #161b22; }
</style>
<div class="logo-text">WORM-GPT</div>
<div class="neon-line"></div>
""", unsafe_allow_html=True)

# --- 3. إدارة الجلسة والبيانات ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_tier = "BASIC"
    st.session_state.page = "Terminal"

# --- 4. نظام تسجيل الدخول (المرتبط بـ database/auth_manager.py) ---
def login_screen():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h3 style='text-align:center;'>🧬 NEURAL ACCESS</h3>", unsafe_allow_html=True)
        serial_input = st.text_input("ENTER ACCESS KEY:", type="password")
        if st.button("UNLOCK SYSTEM", use_container_width=True):
            # سنستخدم دالة التحقق من السيريال من ملف auth_manager لاحقاً
            if serial_input in ["WORM-MASTER-2026", "VIP-99"]: # تجريبي
                st.session_state.authenticated = True
                st.session_state.user_serial = serial_input
                st.rerun()
            else:
                st.error("❌ INVALID SERIAL KEY")
    st.stop()

if not st.session_state.authenticated:
    login_screen()

# --- 5. واجهة التحكم (Sidebar) ---
with st.sidebar:
    st.markdown("### 💀 SYSTEM CORE")
    st.session_state.page = st.radio("Navigation", 
        ["Terminal", "Modules (22)", "Billing/Crypto", "Admin Panel"])
    
    st.divider()
    st.info(f"User: {st.session_state.user_serial}")
    if st.button("LOGOUT"):
        st.session_state.authenticated = False
        st.rerun()

# --- 6. الصفحات الرئيسية ---

# أ. صفحة الشات (Terminal)
if st.session_state.page == "Terminal":
    st.markdown("### 📡 NEURAL TERMINAL")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("State your objective..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.status("💀 EXPLOITING THE MATRIX...", expanded=False):
                # هنا يتم استدعاء ملف core/brain_engine.py
                try:
                    brain = BrainEngine()
                    response = brain.get_response(prompt)
                except:
                    response = "System Error: Brain module not found. Check core/ directory."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# ب. صفحة المدير (Admin Panel)
elif st.session_state.page == "Admin Panel":
    st.markdown("<div class='admin-box'>", unsafe_allow_html=True)
    st.title("⚙️ MASTER CONTROL")
    st.write("Manage serial keys and monitor users here.")
    # سيتم ربطها بـ database/auth_manager.py
    st.markdown("</div>", unsafe_allow_html=True)

# ج. صفحة الموديلات (The 22 Files)
elif st.session_state.page == "Modules (22)":
    st.title("🗂️ SYSTEM MODULES")
    cols = st.columns(2)
    modules_list = [
        "Vision Processor", "Audio Synthesizer", "Search Integrator", 
        "Image Generator", "PDF Analyzer", "Code Executor", 
        "Data Visualizer", "API Rotator", "Performance Monitor"
    ]
    for i, mod in enumerate(modules_list):
        cols[i % 2].checkbox(f"Module: {mod}", value=False, disabled=True)
    st.info("Modules are activated based on your license tier.")
