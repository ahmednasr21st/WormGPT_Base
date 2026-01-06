import streamlit as st
import os

# 1. إعدادات الصفحة (يجب أن تظل في الأعلى)
st.set_page_config(page_title="WORM-GPT ELITE", page_icon="💀", layout="wide")

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
    st.error(f"Module Import Error: {e}")

# تهيئة الكائنات
auth = AuthManager()
styles = StylesManager()
brain = BrainEngine()
history_db = HistoryManager()
vision_mod = VisionProcessor()
pdf_mod = PDFAnalyzer()
img_gen = ImageGenerator()
voice_mod = VoiceSynthesizer()

# تطبيق التصميم
try: styles.apply_global_css()
except: pass

# 3. إدارة الجلسة
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. الشريط الجانبي (Sidebar) ---
# سنقوم بتعريفه هنا ليكون متاحاً دائماً بعد تسجيل الدخول
def draw_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='color:red; text-align:center;'>WORM-GPT CORE</h2>", unsafe_allow_html=True)
        st.divider()
        
        # خيارات التحكم
        st.session_state.search_on = st.toggle("🌐 Live Search", value=False)
        st.session_state.voice_on = st.toggle("🔊 Voice Output", value=False)
        st.session_state.img_mode = st.toggle("🎨 Image Mode", value=False)
        
        st.divider()
        # رفع الملفات
        up_img = st.file_uploader("Scan Image", type=['png', 'jpg', 'jpeg'])
        st.session_state.img_data = vision_mod.process_image_input(up_img)
        
        up_pdf = st.file_uploader("Analyze PDF/TXT", type=['pdf', 'txt'])
        st.session_state.doc_text = None
        if up_pdf:
            st.session_state.doc_text, _ = pdf_mod.extract_text_from_file(up_pdf)
            
        st.divider()
        if st.button("TERMINATE SESSION", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

# --- 5. منطق التشغيل ---
if not st.session_state.authenticated:
    # شاشة تسجيل الدخول
    st.markdown("<h1 style='text-align:center;'>ACCESS REQUIRED</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        serial = st.text_input("ENTER KEY:", type="password")
        if st.button("UNLOCK", use_container_width=True):
            # بصمة الجهاز
            fp = str(st.context.headers.get("User-Agent", "NODE-X"))
            valid, status = auth.verify_serial(serial, fp)
            if valid:
                st.session_state.authenticated = True
                st.session_state.user_serial = serial
                st.session_state.messages = history_db.load_history(serial)
                st.rerun()
            else:
                st.error(f"Error: {status}")
else:
    # إظهار الشريط الجانبي
    draw_sidebar()
    
    # محتوى الشات
    st.markdown(f"### 📡 ACTIVE TERMINAL: `{st.session_state.user_serial}`")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Command..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if st.session_state.get('img_mode'):
                url = img_gen.generate_image(prompt)
                img_gen.display_generated_image(url)
                res = "Image generated."
            else:
                with st.status("💀 THINKING..."):
                    res = brain.get_response(
                        prompt, 
                        image=st.session_state.get('img_data'), 
                        use_search=st.session_state.get('search_on'), 
                        doc_context=st.session_state.get('doc_text')
                    )
                st.markdown(res)
                if st.session_state.get('voice_on'):
                    audio = voice_mod.text_to_speech(res)
                    voice_mod.display_audio_player(audio)
        
        st.session_state.messages.append({"role": "assistant", "content": res})
        history_db.save_history(st.session_state.user_serial, st.session_state.messages)
