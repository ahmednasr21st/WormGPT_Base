import streamlit as st

class StylesManager:
    @staticmethod
    def apply_global_css():
        st.markdown("""
        <style>
            /* تخصيص الخلفية والألوان لتشبه Gemini المظلم */
            .stApp {
                background-color: #131314;
                color: #e3e3e3;
            }
            [data-testid="stSidebar"] {
                background-color: #1e1f20;
            }
            .stTextInput input {
                background-color: #282a2d !important;
                color: white !important;
                border: 1px solid #3c4043 !important;
            }
            .stButton button {
                background-color: #4285f4 !important;
                color: white !important;
                border-radius: 10px;
            }
        </style>
        """, unsafe_allow_html=True)