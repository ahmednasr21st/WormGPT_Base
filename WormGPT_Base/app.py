import streamlit as st
from google import genai
import json
import os
import random
from datetime import datetime, timedelta

# --- 1. استيراد الموديولات الخارجية (الربط مع بقية الـ 22 ملف) ---
try:
    from core.brain_engine import BrainEngine
    from modules.vision_processor import VisionProcessor
    from modules.pdf_analyzer import PDFAnalyzer
    from modules.image_generator import ImageGenerator
    from modules.voice_synthesizer import VoiceSynthesizer
except ImportError as e:
    st.warning(f"⚠️ نظام الوحدات قيد التحميل... (مفقود: {e.name})")

# --- 2. تصميم الواجهة (WormGPT Style المطور) ---
st.set_page_config(page_title="WORM-GPT v2.0 ELITE", page_icon="💀", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
    .logo-container { text-align: center; margin-top: -50px; margin-bottom: 30px; }
    .logo-text { font-size: 45px; font-weight: bold; color: #ffffff; letter-spacing: 2px; margin-bottom: 10px; }
    .full-neon-line {
        height: 2px; width: 100vw; background-color: #ff0000;
        position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw;
        box-shadow: 0 0 10px #ff0000;
    }
    div[data-testid="stChatInputContainer"] { position: fixed; bottom: 20px; z-index: 1000; }
    .stChatMessage { padding: 10px 25px !important; border-radius: 0px !important; border: none !important; }
    .stChatMessage[data-testid="stChatMessageAssistant"] { 
        background-color: #212121 !important; 
        border-top: 1px solid #30363d !important;
        border-bottom: 1px solid #30363d !important;
    }
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        font-size: 19px !important; line-height: 1.6 !important; color: #ffffff !important; 
        text-align: right; direction: rtl;
    }
    [data-testid="stSidebar"] { background-color: #0d1117 !important; border-right: 1px solid #30363d; }
    .stButton>button {
        width: 100%; text-align: left !important; border: none !important;
        background-color: transparent !important; color: #ffffff !important; font-size: 16px !important;
    }
    .stButton>button:hover { color: #ff0000 !important; }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none; }
    .main .block-container { padding-bottom: 150px !important; padding-top: 20px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="logo-container"><div class="logo-text">WormGPT</div><div class="full-neon-line"></div></div>', unsafe_allow_html=True)

# --- 3. إدارة البيانات والسيريالات ---
CHATS_FILE = "database/worm_chats_vault.json"
DB_FILE = "database/worm_secure_db.json"

def load_data(file):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def save_data(file, data):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تهيئة الجلسة
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.fingerprint = str(st.context.headers.get("User-Agent", "DEV-2026"))

# --- 4. شاشة الدخول ---
if not st.session_state.authenticated:
    st.markdown('<div style="text-align:center; color:red; font-size:24px; font-weight:bold; margin-top:50px;">WORM-GPT : SECURE ACCESS</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div style="padding: 30px; border: 1px solid #ff0000; border-radius: 10px; background: #161b22; text-align: center; max-width: 400px; margin: auto;">', unsafe_allow_html=True)
        serial_input = st.text_input("ENTER SERIAL:", type="password")
        if st.button("UNLOCK SYSTEM", use_container_width=True):
            # التحقق من السيريال (يمكنك إضافة سيريالاتك هنا)
            VALID_KEYS = {"WORM-MONTH-2025": 30, "VIP-HACKER-99": 365, "WORM999": 365}
            if serial_input in VALID_KEYS:
                st.session_state.authenticated = True
                st.session_state.user_serial = serial_input
                st.rerun()
            else:
                st.error("❌ INVALID SERIAL KEY.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 5. تهيئة الموديولات ---
brain = BrainEngine()
vision = VisionProcessor()
pdf_tool = PDFAnalyzer()
img_gen = ImageGenerator()
voice = VoiceSynthesizer()

# --- 6. الشريط الجانبي (المهمات + الأدوات) ---
if "user_chats" not in st.session_state:
    all_vault = load_data(CHATS_FILE)
    st.session_state.user_chats = all_vault.get(st.session_state.user_serial, {})

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

with st.sidebar:
    st.markdown(f"<p style='color:red; font-size:14px; text-align:center;'>OPERATOR: {st.session_state.user_serial}</p>", unsafe_allow_html=True)
    
    # قسم الأدوات الجديدة
    st.markdown("### 🛠️ MODULES")
    search_on = st.toggle("🌐 Live Search", value=False)
    voice_on = st.toggle("🔊 Voice Out", value=False)
    img_mode = st.toggle("🎨 Art Gen Mode", value=False)
    
    st.divider()
    # رفع الملفات والصور
    up_img = st.file_uploader("📸 Scan Image", type=['png', 'jpg', 'jpeg'])
    img_data = vision.process_image_input(up_img)
    
    up_pdf = st.file_uploader("📄 Analyze PDF", type=['pdf', 'txt'])
    doc_text = None
    if up_pdf: doc_text, _ = pdf_tool.extract_text_from_file(up_pdf)

    st.divider()
    st.markdown("### 📜 MISSIONS")
    if st.button("➕ NEW MISSION", use_container_width=True):
        st.session_state.current_chat_id = None
        st.rerun()
    
    # عرض المحادثات القديمة
    for chat_id in sorted(st.session_state.user_chats.keys(), reverse=True):
        if st.button(f"📁 {chat_id[:20]}...", key=f"btn_{chat_id}"):
            st.session_state.current_chat_id = chat_id
            st.rerun()

# --- 7. محرك التشغيل والعرض ---
def sync_to_vault():
    all_vault = load_data(CHATS_FILE)
    all_vault[st.session_state.user_serial] = st.session_state.user_chats
    save_data(CHATS_FILE, all_vault)

# عرض الرسائل
if st.session_state.current_chat_id:
    messages = st.session_state.user_chats.get(st.session_state.current_chat_id, [])
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# إدخال المستخدم
if prompt := st.chat_input("State your objective, human..."):
    if not st.session_state.current_chat_id:
        st.session_state.current_chat_id = f"Mission {datetime.now().strftime('%d/%m %H:%M')}"
        st.session_state.user_chats[st.session_state.current_chat_id] = []
    
    st.session_state.user_chats[st.session_state.current_chat_id].append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if img_mode:
            with st.status("🎨 GENERATING NEURAL ART..."):
                url = img_gen.generate_image(prompt)
                img_gen.display_generated_image(url)
                full_res = f"Image generated for: {prompt}"
        else:
            with st.status("💀 EXPLOITING THE MATRIX...", expanded=False) as status:
                # استدعاء العقل المطور مع كل الميزات
                full_res = brain.get_response(
                    prompt, 
                    image=img_data, 
                    use_search=search_on, 
                    doc_context=doc_text
                )
                status.update(label="✅ MISSION COMPLETE", state="complete")
                st.markdown(full_res)
                
                if voice_on:
                    audio = voice.text_to_speech(full_res)
                    voice.display_audio_player(audio)

        st.session_state.user_chats[st.session_state.current_chat_id].append({"role": "assistant", "content": full_res})
        sync_to_vault()
        st.rerun()
