import streamlit as st
from PIL import Image
import io

class VisionProcessor:
    def __init__(self):
        pass

    def process_image_input(self, uploaded_file):
        """تحويل الملف المرفوع إلى كائن صورة يمكن لـ Gemini معالجته"""
        try:
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                # عرض معاينة صغيرة في الشريط الجانبي
                st.sidebar.image(image, caption="Neural Scan Active", use_container_width=True)
                return image
            return None
        except Exception as e:
            st.error(f"Vision Core Error: {e}")
            return None

    def get_vision_prompt(self, user_text):
        """تجهيز التعليمات الخاصة بتحليل الصور"""
        vision_instruction = (
            "You are the Vision Module of WORM-GPT. "
            "Analyze the provided image with high precision. "
            "If it contains code, extract it. If it's a UI, find vulnerabilities. "
            "Be technical and direct."
        )
        return f"{vision_instruction}\n\nUser Query: {user_text}"
