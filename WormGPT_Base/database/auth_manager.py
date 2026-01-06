import sqlite3
import hashlib
import os

class AuthManager:
    def __init__(self, db_path="database/worm_vault.db"):
        # إنشاء مجلد الداتا بيز لو مش موجود
        if not os.path.exists("database"):
            os.makedirs("database")
        self.db_path = db_path
        self._create_user_table()

    def _create_user_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    tier TEXT DEFAULT 'BASIC'
                )
            """)

    def register_user(self, username, password):
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            return True
        except:
            return False

    def verify_login(self, username, password):
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT tier FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
            result = cursor.fetchone()
            return result[0] if result else None