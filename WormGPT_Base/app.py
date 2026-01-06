import streamlit as st
import os
from datetime import datetime

# --- 1. استيراد المحركات ---
try:
    from database.auth_manager import AuthManager
    from core.styles_manager import StylesManager
    from core.brain_engine import BrainEngine
    from modules.history_manager import HistoryManager
    from modules.vision_processor import VisionProcessor # الموديل الجديد
except ImportError as e:
    st.error(f"❌ Missing Module: {e}")
    st.stop()

# --- 2. إعدادات الصفحة ---
st.set_page_config(page_title="WORM-GPT v2.0", page_icon="💀", layout="wide")

auth = AuthManager()
styles = StylesManager()
brain = BrainEngine()
history_db = HistoryManager()
vision_mod = VisionProcessor()

styles.apply_global_css()

# --- 3. إدارة الجلسة ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_serial" not in st.session_state:
    st.session_state.user_serial = None

fingerprint = str(st.context.headers.get("User-Agent", "NODE-01"))

# --- 4. واجهة تسجيل الدخول ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center; color:white;'>🧬 WORM-GPT ACCESS</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        serial_input = st.text_input("SERIAL KEY:", type="password")
        if st.button("UNLOCK CORE", use_container_width=True):
            is_valid, status = auth.verify_serial(serial_input, fingerprint)
            if is_valid:
                st.session_state.authenticated = True
                st.session_state.user_serial = serial_input
                st.session_state.messages = history_db.load_history(serial_input)
                st.rerun()
            else:
                st.error(f"Access Denied: {status}")
    st.stop()

# --- 5. الواجهة الرئيسية (Terminal) ---
with st.sidebar:
    st.markdown("<h2 style='color:red; text-align:center;'>WORM-GPT</h2>", unsafe_allow_html=True)
    st.divider()
    
    # قسم الرؤية (Vision Module)
    st.markdown("### 📸 VISION CORE")
    uploaded_img = st.file_uploader("Upload Image for Analysis", type=['png', 'jpg', 'jpeg'])
    processed_img = vision_mod.process_image_input(uploaded_img)
    
    st.divider()
    if st.button("NEW MISSION", use_container_width=True):
        history_db.clear_history(st.session_state.user_serial)
        st.session_state.messages = []
        st.rerun()
    
    if st.button("LOGOUT"):
        st.session_state.authenticated = False
        st.rerun()

# عرض الشات
st.markdown("### 📡 NEURAL TERMINAL")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# إرسال الأوامر (دعم النص والصور)
if prompt := st.chat_input("State your objective..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("💀 PROCESSING NEURAL DATA...", expanded=False) as status:
            # إرسال الصورة للمحرك إذا كانت موجودة
            response = brain.get_response(prompt, image=processed_img)
            status.update(label="✅ ANALYSIS COMPLETE", state="complete")
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    history_db.save_history(st.session_state.user_serial, st.session_state.messages)

