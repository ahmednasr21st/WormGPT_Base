import streamlit as st
import os

# 1. إعدادات الصفحة (يجب أن يكون أول أمر في السكربت)
st.set_page_config(
    page_title="WORM-GPT ELITE",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- علامة التحقق من التحديث (لو ظهرت يعني السيرفر قرأ الكود الجديد) ---
st.caption("🚀 Neural System Version: 5.0.1 - Active")

# 2. استيراد المحركات (Modules) مع معالجة الأخطاء
try:
    from database.auth_manager import AuthManager
    from core.styles_manager import StylesManager
    from core.brain_engine import BrainEngine
    
    auth = AuthManager()
    styles = StylesManager()
except ImportError as e:
    st.error(f"❌ Error loading modules: {e}")
    st.info("تأكد من وجود ملفات __init__.py داخل مجلد core و database")
    st.stop()

# 3. تطبيق التصميم المظلم فوراً
styles.apply_global_css()

# 4. إدارة حالة الجلسة (Session State)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------------------------------------
# 5. واجهة تسجيل الدخول (Login UI)
# ------------------------------------------------------------------------------
def render_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center; color: #4285f4;'>🧬 WORM-GPT</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["[ LOGIN ]", "[ SIGN UP ]"])
        
        with tab1:
            u = st.text_input("Username", placeholder="Enter ID...")
            p = st.text_input("Password", type="password", placeholder="Enter Access Code...")
            if st.button("UNLOCK ACCESS", use_container_width=True):
                tier = auth.verify_login(u, p)
                if tier:
                    st.session_state.authenticated = True
                    st.session_state.username = u
                    st.session_state.tier = tier
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid Credentials")
                    
        with tab2:
            new_u = st.text_input("New Identity")
            new_p = st.text_input("New Access Code", type="password")
            if st.button("CREATE ACCOUNT", use_container_width=True):
                if auth.register_user(new_u, new_p):
                    st.success("Identity Created. Proceed to Login.")
                else:
                    st.error("Identity already exists in database.")

# ------------------------------------------------------------------------------
# 6. واجهة الشات والذكاء (Main Interface)
# ------------------------------------------------------------------------------
def render_chat():
    # الشريط الجانبي (Sidebar)
    with st.sidebar:
        st.title("💀 WORM-GPT")
        st.markdown(f"**Operator:** `{st.session_state.username}`")
        st.markdown(f"**Tier:** `{st.session_state.tier}`")
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # عرض الرسائل السابقة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # استقبال أوامر المستخدم
    if prompt := st.chat_input("Enter Command to Neural Core..."):
        # عرض رسالة المستخدم
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # استدعاء عقل Gemini للحصول على الرد
        with st.chat_message("assistant"):
            try:
                brain = BrainEngine()
                with st.spinner("Processing Neural Request..."):
                    response = brain.get_response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Brain Sync Error: {e}")

# ------------------------------------------------------------------------------
# 7. التشغيل الفعلي (Main Logic)
# ------------------------------------------------------------------------------
if not st.session_state.authenticated:
    render_login()
else:
    render_chat()
