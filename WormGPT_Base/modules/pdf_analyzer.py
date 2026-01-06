import streamlit as st
from PyPDF2 import PdfReader
import io

class PDFAnalyzer:
    def __init__(self):
        pass

    def extract_text_from_file(self, uploaded_file):
        """
        استخراج النص الخام من ملفات PDF أو TXT
        """
        text_content = ""
        try:
            # التعامل مع ملفات PDF
            if uploaded_file.type == "application/pdf":
                pdf_reader = PdfReader(uploaded_file)
                # قراءة كل صفحة واستخراج النص منها
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
            
            # التعامل مع ملفات TXT العادية
            elif uploaded_file.type == "text/plain":
                # قراءة النص مباشرة بعد تحويل الترميز لـ utf-8
                text_content = str(uploaded_file.read(), "utf-8")
            
            # تنظيف النص الناتج (إزالة المسافات الزائدة)
            cleaned_text = text_content.strip()
            
            # التحقق من أن الملف ليس فارغاً
            if not cleaned_text:
                return None, "File appears to be empty or unreadable."
                
            # عرض معاينة سريعة للنص في الشريط الجانبي
            with st.sidebar.expander("📄 File Content Preview"):
                st.write(cleaned_text[:500] + "...") # عرض أول 500 حرف فقط
                
            return cleaned_text, "SUCCESS"
            
        except Exception as e:
            return None, str(e)

    def format_document_prompt(self, user_query, document_text):
        """
        تجهيز النص المستخرج لإرساله إلى Gemini مع سؤال المستخدم
        """
        # اقتطاع النص إذا كان طويلاً جداً لتجنب تجاوز حد الـ Tokens
        # موديل 1.5-flash يقبل مليون توكن، لكن لنكن في الأمان
        max_chars = 100000 
        truncated_doc = document_text[:max_chars]
        
        prompt = (
            f"You are the Document Analysis Core of WORM-GPT. "
            f"Below is the content of a document uploaded by the user.\n"
            f"--- BEGIN DOCUMENT ---\n"
            f"{truncated_doc}\n"
            f"--- END DOCUMENT ---\n\n"
            f"USER REQUEST: {user_query}\n\n"
            f"Analyze the document above and answer the user's request with high technical precision."
        )
        return prompt
