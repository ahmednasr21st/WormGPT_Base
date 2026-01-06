from gtts import gTTS
import io
import streamlit as st

class VoiceSynthesizer:
    def __init__(self):
        # اللغات المدعومة
        self.lang_map = {
            "English": "en",
            "Arabic": "ar"
        }

    def text_to_speech(self, text, lang="English"):
        """تحويل النص إلى ملف صوتي في الذاكرة"""
        try:
            # اختيار كود اللغة
            lang_code = self.lang_map.get(lang, "en")
            
            # توليد الصوت
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            # حفظ الصوت في كائن "بايت" بدلاً من ملف على القرص
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            
            return audio_fp
        except Exception as e:
            st.error(f"Voice Synthesis Error: {e}")
            return None

    def display_audio_player(self, audio_data):
        """عرض مشغل الصوت في واجهة Streamlit"""
        if audio_data:
            st.audio(audio_data, format="audio/mp3")
