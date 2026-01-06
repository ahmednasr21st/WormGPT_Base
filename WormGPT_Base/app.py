import streamlit as st
import os
from datetime import datetime

# --- 1. استيراد المحركات الخاصة بنا ---
try:
    from database.auth_manager import AuthManager
    from core.styles_manager import StylesManager
    from core.brain_engine import BrainEngine
    from modules.history_manager import HistoryManager
except ImportError as e:
    st.error(f"❌ Critical Error: Missing Module {e}")
    st.stop()

# --- 2. إعدادات الصفحة الأولية ---
st.set_page_config(
    page_title="WORM-GPT v2.0 ELITE",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. تهيئة الكائنات (Objects) ---
auth = AuthManager()
styles = StylesManager()
brain = BrainEngine()
history_db = HistoryManager()

# تطبيق التصميم فوراً
styles.apply_global_css()

# --- 4. إدارة حالة الجلسة (Session State) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_serial" not in st.session_state:
    st.session_state.user_serial = None
if "page" not in st.session_state:
    st.session_state.page = "Terminal"

# بصمة الجهاز البسيطة (للتأكد من القفل)
fingerprint = str(st.context.headers.get("User-Agent", "NODE-01"))

# --- 5. واجهة تسجيل الدخول (Login UI) ---
def render_login():
    st.markdown("<div style='text-align:center; padding-top:100px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:white; font-size:50px;'>WORM-GPT</h1>", unsafe_allow_html=True)
    st.markdown("<div style='height:2px; background:red; box-shadow:0 0 10px red; margin: 20px auto; width:50%;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        serial_input = st.text_input("ENTER ACCESS KEY:", type="password", placeholder="WORM-XXXX-XXXX")
        if st.button("UNLOCK NEURAL CORE", use_container_width=True):
            is_valid, status = auth.verify_serial(serial_input, fingerprint)
            if is_valid:
                st.session_state.authenticated = True
                st.session_state.user_serial = serial_input
                # تحميل التاريخ عند تسجيل الدخول الناجح
                st.session_state.messages = history_db.load_history(serial_input)
                st.rerun()
            else:
                if status == "EXPIRED": st.error("❌ Subscription Expired.")
                elif status == "LOCKED_TO_OTHER_DEVICE": st.error("❌ Access Locked to another hardware ID.")
                else: st.error("❌ Invalid Access Key.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. الواجهة الرئيسية بعد الدخول ---
def render_main():
    # الشريط الجانبي (Sidebar)
    with st.sidebar:
        st.markdown("<h2 style='color:red; text-align:center;'>CONTROL</h2>", unsafe_allow_html=True)
        st.divider()
        
        st.session_state.page = st.radio("NAVIGATION", 
            ["Terminal", "System Modules", "Admin Panel"], index=0)
        
        st.divider()
        st.write(f"🧬 **Serial:** `{st.session_state.user_serial}`")
        st.write(f"🛰️ **Status:** `Encrypted Connection`")
        
        if st.button("TERMINATE SESSION", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # أ. صفحة الشات (Terminal)
    if st.session_state.page == "Terminal":
        st.markdown("<h3 style='color:red;'>📡 NEURAL TERMINAL ACTIVE</h3>", unsafe_allow_html=True)
        
        # عرض الرسائل المخزنة
        if "messages" not in st.session_state:
            st.session_state.messages = history_db.load_history(st.session_state.user_serial)

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # استقبال الأوامر
        if prompt := st.chat_input("State your objective, Operator..."):
            # عرض رسالة المستخدم
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # طلب الرد من محرك الذكاء
            with st.chat_message("assistant"):
                with st.status("💀 BYPASSING PROTOCOLS...", expanded=False) as status:
                    response = brain.get_response(prompt)
                    status.update(label="✅ RESPONSE SECURED", state="complete")
                    st.markdown(response)
            
            # حفظ الرد في التاريخ والجلسة
            st.session_state.messages.append({"role": "assistant", "content": response})
            history_db.save_history(st.session_state.user_serial, st.session_state.messages)

    # ب. صفحة الموديلات
    elif st.session_state.page == "System Modules":
        st.title("🗂️ NEURAL MODULES (22)")
        st.info("These modules are being integrated. Version 2.0.1")
        cols = st.columns(3)
        modules = ["Vision", "Audio", "Scanner", "Search", "Code Exploit", "Crypto Pay"]
        for i, m in enumerate(modules):
            cols[i%3].checkbox(m, value=True if i==0 else False, disabled=True)

    # ج. لوحة المدير
    elif st.session_state.page == "Admin Panel":
        st.title("⚙️ MASTER CONTROL")
        admin_pass = st.text_input("Enter Admin Credentials:", type="password")
        if admin_pass == st.secrets.get("ADMIN_PASSWORD", "WORM_ADMIN"):
            st.success("Welcome, Architect.")
            # هنا يمكنك إضافة كود إدارة السيريالات لاحقاً
        else:
            st.warning("Unauthorized Access Attempt Detected.")

# --- 7. التشغيل الفعلي ---
if not st.session_state.authenticated:
    render_login()
else:
    render_main()
