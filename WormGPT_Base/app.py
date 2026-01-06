import streamlit as st
import os

# --- 1. استيراد كافة المحركات (الـ 12 موديول) ---
try:
    from database.auth_manager import AuthManager
    from core.styles_manager import StylesManager
    from core.brain_engine import BrainEngine
    from modules.history_manager import HistoryManager
    from modules.vision_processor import VisionProcessor
    from modules.pdf_analyzer import PDFAnalyzer
    from modules.image_generator import ImageGenerator
    from modules.voice_synthesizer import VoiceSynthesizer
except ImportError as e:
    st.error(f"⚠️ System Warning: Some modules are still initializing... ({e.name})")

# --- 2. إعدادات المنصة ---
st.set_page_config(page_title="WORM-GPT ELITE v4", page_icon="💀", layout="wide")

# تهيئة الكائنات الأساسية
auth = AuthManager()
styles = StylesManager()
brain = BrainEngine()
history_db = HistoryManager()
vision_mod = VisionProcessor()
pdf_mod = PDFAnalyzer()
img_gen = ImageGenerator()
voice_mod = VoiceSynthesizer()

# تطبيق التصميم النيوني
try: styles.apply_global_css()
except: pass

# --- 3. إدارة الجلسة ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []

fingerprint = str(st.context.headers.get("User-Agent", "NODE-X"))

# --- 4. بوابة الدخول ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center;'>WORM-GPT</h1>", unsafe_allow_html=True)
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
                st.error(f"DENIED: {status}")
    st.stop()

# --- 5. لوحة التحكم المتقدمة (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color:red; text-align:center;'>CORE SYSTEMS</h2>", unsafe_allow_html=True)
    st.divider()
    
    # خيارات البحث والصوت
    st.markdown("### 🛠️ SETTINGS")
    search_on = st.toggle("🌐 Live Web Search", value=False)
    voice_on = st.toggle("🔊 Neural Voice Output", value=False)
    img_mode = st.toggle("🎨 Image Generation Mode", value=False)
    
    # رفع الصور والملفات
    st.divider()
    st.markdown("### 📂 UPLOADS")
    uploaded_img = st.file_uploader("Upload Image (Vision)", type=['png', 'jpg', 'jpeg'])
    img_data = vision_mod.process_image_input(uploaded_img)
    
    uploaded_pdf = st.file_uploader("Upload Document (PDF/TXT)", type=['pdf', 'txt'])
    doc_text = None
    if uploaded_pdf:
        doc_text, pdf_status = pdf_mod.extract_text_from_file(uploaded_pdf)
    
    st.divider()
    if st.button("TERMINATE SESSION"):
        st.session_state.authenticated = False
        st.rerun()

# --- 6. محطة الدردشة (Terminal) ---
st.markdown(f"### 📡 TERMINAL: `{st.session_state.user_serial}`")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Enter command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # حالة التوليد الصوري
        if img_mode:
            with st.spinner("🎨 Generating Art..."):
                img_url = img_gen.generate_image(prompt)
                img_gen.display_generated_image(img_url)
                response = f"Image generated for: {prompt}"
        else:
            # حالة الرد الذكي (نصوص/ملفات/بحث)
            with st.status("💀 PROCESSING...", expanded=False) as status:
                response = brain.get_response(
                    prompt, 
                    image=img_data, 
                    use_search=search_on, 
                    doc_context=doc_text
                )
                status.update(label="✅ COMPLETE", state="complete")
            st.markdown(response)
            
            # تفعيل النطق الصوتي إذا كان مختاراً
            if voice_on:
                audio = voice_mod.text_to_speech(response)
                voice_mod.display_audio_player(audio)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    history_db.save_history(st.session_state.user_serial, st.session_state.messages)
