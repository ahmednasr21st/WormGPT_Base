import plotly.express as px
import pandas as pd
import streamlit as st

class DataVisualizer:
    def __init__(self):
        # إعداد ثيم داكن يتناسب مع تصميم الموقع
        self.template = "plotly_dark"
        self.color_sequence = ["#ff0000", "#ff4b4b", "#8b0000", "#5f0000"]

    def create_bar_chart(self, data_dict, title="Statistical Analysis", x_label="Category", y_label="Value"):
        """إنشاء مخطط أعمدة تفاعلي"""
        try:
            df = pd.DataFrame(list(data_dict.items()), columns=[x_label, y_label])
            fig = px.bar(
                df, x=x_label, y=y_label, 
                title=title,
                template=self.template,
                color_discrete_sequence=self.color_sequence
            )
            return fig
        except Exception as e:
            st.error(f"Visualization Error (Bar): {e}")
            return None

    def create_pie_chart(self, data_dict, title="Data Distribution"):
        """إنشاء مخطط دائري"""
        try:
            df = pd.DataFrame(list(data_dict.items()), columns=["Label", "Value"])
            fig = px.pie(
                df, names="Label", values="Value", 
                title=title,
                template=self.template,
                color_discrete_sequence=self.color_sequence,
                hole=0.4 # لجعله بشكل Donut عصري
            )
            return fig
        except Exception as e:
            st.error(f"Visualization Error (Pie): {e}")
            return None

    def display_chart(self, figure):
        """عرض المخطط داخل Streamlit"""
        if figure:
            st.plotly_chart(figure, use_container_width=True)
