import streamlit as st
import os
from datetime import datetime

# --- 1. استيراد المحركات مع معالجة الأخطاء (Future-Proof) ---
try:
    from database.auth_manager import AuthManager
    from core.styles_manager import StylesManager
    from core.brain_engine import BrainEngine
    from modules.history_manager import HistoryManager
    from modules.vision_processor import VisionProcessor
except ImportError as e:
    st.error(f"⚠️ Initializing System Components... (Missing: {e.name})")

# --- 2. إعدادات المنصة ---
st.set_page_config(page_title="WORM-GPT ELITE", page_icon="💀", layout="wide")

# تهيئة الكائنات
auth = AuthManager()
styles = StylesManager()
brain = BrainEngine()
history_db = HistoryManager()
vision_mod = VisionProcessor()

# تطبيق الثيم النيوني
try: styles.apply_global_css()
except: pass

# --- 3. إدارة الجلسة ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_serial" not in st.session_state:
    st.session_state.user_serial = None
if "messages" not in st.session_state:
    st.session_state.messages = []

fingerprint = str(st.context.headers.get("User-Agent", "NODE-X"))

# --- 4. بوابة الدخول الأمنية ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center; color:white; letter-spacing:5px;'>WORM-GPT</h1>", unsafe_allow_html=True)
    st.markdown("<div style='height:2px; background:red; box-shadow:0 0 15px red; margin-bottom:30px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        serial_input = st.text_input("NEURAL ACCESS KEY:", type="password")
        if st.button("BYPASS SECURITY", use_container_width=True):
            is_valid, status = auth.verify_serial(serial_input, fingerprint)
            if is_valid:
                st.session_state.authenticated = True
                st.session_state.user_serial = serial_input
                st.session_state.messages = history_db.load_history(serial_input)
                st.rerun()
            else:
                st.error(f"ACCESS DENIED: {status}")
    st.stop()

# --- 5. لوحة التحكم الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color:red; text-align:center;'>TERMINAL CONTROL</h2>", unsafe_allow_html=True)
    st.divider()
    
    # موديول البحث الحي
    st.markdown("### 🌐 NETWORK ACCESS")
    search_enabled = st.toggle("Live Web Search", value=False)
    
    # موديول الرؤية
    st.markdown("### 📸 VISION CORE")
    img_file = st.file_uploader("Upload Target Image", type=['png', 'jpg', 'jpeg'])
    processed_img = vision_mod.process_image_input(img_file)
    
    st.divider()
    # موديولات قادمة (أزرار جاهزة)
    st.markdown("### 🛠️ ADVANCED TOOLS")
    img_gen_mode = st.toggle("Image Generation Mode", value=False)
    deep_scan = st.toggle("Deep File Analysis", value=False)
    
    st.divider()
    if st.button("DELETE NEURAL LOGS (Clear)"):
        history_db.clear_history(st.session_state.user_serial)
        st.session_state.messages = []
        st.rerun()
    
    if st.button("TERMINATE SESSION"):
        st.session_state.authenticated = False
        st.rerun()

# --- 6. محطة الدردشة الرئيسية ---
st.markdown(f"### 📡 LOGGED AS: `{st.session_state.user_serial}`")

# عرض التاريخ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# استقبال الأوامر
if prompt := st.chat_input("Enter command to WormGPT..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("💀 EXPLOITING PROTOCOLS...", expanded=False) as status:
            # استدعاء المحرك مع كل الميزات الممكنة
            response = brain.get_response(
                prompt, 
                image=processed_img, 
                use_search=search_enabled,
                is_gen_mode=img_gen_mode
            )
            status.update(label="✅ TASK COMPLETED", state="complete")
            st.markdown(response)
    
    # حفظ التاريخ
    st.session_state.messages.append({"role": "assistant", "content": response})
    history_db.save_history(st.session_state.user_serial, st.session_state.messages)
