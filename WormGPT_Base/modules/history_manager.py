import json
import os
import streamlit as st

class HistoryManager:
    def __init__(self, history_dir="database/vault_history"):
        self.history_dir = history_dir
        # إنشاء مجلد الحفظ إذا لم يكن موجوداً
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)

    def get_user_file(self, user_serial):
        """تحديد مسار ملف التاريخ الخاص بكل مستخدم"""
        return os.path.join(self.history_dir, f"{user_serial}_history.json")

    def load_history(self, user_serial):
        """تحميل سجل المحادثات من الملف"""
        file_path = self.get_user_file(user_serial)
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self, user_serial, messages):
        """حفظ سجل المحادثات في ملف JSON"""
        file_path = self.get_user_file(user_serial)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            st.error(f"Error saving neural logs: {e}")
            return False

    def clear_history(self, user_serial):
        """مسح السجل لبدء مهمة جديدة"""
        file_path = self.get_user_file(user_serial)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False