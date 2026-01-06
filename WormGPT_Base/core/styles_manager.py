import streamlit as st

class StylesManager:
    @staticmethod
    def apply_global_css():
        """تطبيق التصميم السيبراني على كامل الموقع"""
        st.markdown("""
        <style>
            /* 1. الخلفية العامة والخطوط */
            @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500&display=swap');
            
            .stApp {
                background-color: #08090a;
                color: #e6edf3;
                font-family: 'Fira Code', monospace;
            }

            /* 2. تخصيص القائمة الجانبية (Sidebar) */
            [data-testid="stSidebar"] {
                background-color: #0d1117 !important;
                border-right: 2px solid #ff0000;
                box-shadow: 5px 0px 15px rgba(255, 0, 0, 0.2);
            }

            /* 3. تخصيص فقاعات الشات (Chat Bubbles) */
            .stChatMessage {
                background-color: #161b22 !important;
                border: 1px solid #30363d !important;
                border-radius: 5px !important;
                margin-bottom: 10px !important;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
            }
            
            /* تأثير النيون عند الوقوف على الرسائل */
            .stChatMessage:hover {
                border-color: #ff0000 !important;
                transition: 0.3s;
            }

            /* 4. تخصيص شريط الإدخال (Input Bar) */
            div[data-testid="stChatInputContainer"] {
                background-color: #0d1117 !important;
                border: 1px solid #ff0000 !important;
                border-radius: 10px !important;
                padding: 5px !important;
            }

            /* 5. الأزرار الاحترافية */
            .stButton>button {
                background-color: transparent !important;
                color: #ff0000 !important;
                border: 1px solid #ff0000 !important;
                font-weight: bold !important;
                text-transform: uppercase;
                letter-spacing: 2px;
                transition: 0.4s;
            }

            .stButton>button:hover {
                background-color: #ff0000 !important;
                color: white !important;
                box-shadow: 0 0 20px #ff0000;
            }

            /* 6. إخفاء العناصر غير الضرورية لمظهر أكثر نظافة */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}

            /* 7. شريط الحالة (Status) */
            .stStatus {
                background-color: #0d1117 !important;
                color: #ff0000 !important;
                border: 1px solid #ff0000 !important;
            }
        </style>
        """, unsafe_allow_html=True)
