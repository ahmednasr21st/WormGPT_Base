import streamlit as st
import os

# 1. إعدادات الصفحة (يجب أن يكون أول أمر)
st.set_page_config(
    page_title="WORM-GPT ELITE",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="expanded" # تأكد أنها expanded
)

# 2. استيراد المحركات
try:
    from database.auth_manager import AuthManager
    from core.styles_manager import StylesManager
    from core.brain_engine import BrainEngine
    from modules.history_manager import HistoryManager
    from modules.vision_processor import VisionProcessor
    from modules.pdf_analyzer import PDFAnalyzer
    from modules.image_generator import ImageGenerator
    from modules.voice_synthesizer import VoiceSynthesizer
except Exception as e:
    st.warning(f"🔄 Booting System Modules... (Waiting for: {str(e)})")

# تهيئة الكائنات
auth = AuthManager()
styles = StylesManager()
brain = BrainEngine()
history_db = HistoryManager()
vision_mod = VisionProcessor()
pdf_mod = PDFAnalyzer()
img_gen = ImageGenerator()
voice_mod = VoiceSynthesizer()

# تطبيق التصميم (تأكد أن ملف styles_manager لا يخفي الـ sidebar)
try:
    styles.apply_global_css()
except:
    pass

# 3. إدارة الجلسة
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []

fingerprint = str(st.context.headers.get("User-Agent", "NODE-X"))

# ---------------------------------------------------------
# 4. منطق العرض (Execution Logic)
# ---------------------------------------------------------

if not st.session_state.authenticated:
    # شاشة تسجيل الدخول (بدون شريط جانبي لتركيز المستخدم)
    st.markdown("<h1 style='text-align:center;'>WORM-GPT ACCESS</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        serial_input = st.text_input("NEURAL ACCESS KEY:", type="password")
        if st.button("UNLOCK SYSTEM", use_container_width=True):
            is_valid, status = auth.verify_serial(serial_input, fingerprint)
            if is_valid:
                st.session_state.authenticated = True
                st.session_state.user_serial = serial_input
                st.session_state.messages = history_db.load_history(serial_input)
                st.rerun()
            else:
                st.error(f"DENIED: {status}")
else:
    # الشريط الجانبي يظهر فقط هنا (بعد النجاح)
    with st.sidebar:
        st.markdown("<h2 style='color:red; text-align:center;'>CORE SYSTEMS</h2>", unsafe_allow_html=True)
        st.divider()
        
        search_on = st.toggle("🌐 Live Web Search", value=False)
        voice_on = st.toggle("🔊 Neural Voice Output", value=False)
        img_mode = st.toggle("🎨 Image Generation Mode", value=False)
        
        st.divider()
        uploaded_img = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
        img_data = vision_mod.process_image_input(uploaded_img)
        
        uploaded_pdf = st.file_uploader("Upload PDF/TXT", type=['pdf', 'txt'])
        doc_text = None
        if uploaded_pdf:
            doc_text, _ = pdf_mod.extract_text_from_file(uploaded_pdf)
            
        if st.button("TERMINATE SESSION"):
            st.session_state.authenticated = False
            st.rerun()

    # محتوى الشات الرئيسي
    st.markdown(f"### 📡 TERMINAL: `{st.session_state.user_serial}`")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Enter command..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if img_mode:
                img_url = img_gen.generate_image(prompt)
                img_gen.display_generated_image(img_url)
                response = f"Art generated for: {prompt}"
            else:
                with st.status("💀 PROCESSING...", expanded=False):
                    response = brain.get_response(prompt, image=img_data, use_search=search_on, doc_context=doc_text)
                st.markdown(response)
                if voice_on:
                    audio = voice_mod.text_to_speech(response)
                    voice_mod.display_audio_player(audio)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        history_db.save_history(st.session_state.user_serial, st.session_state.messages)
