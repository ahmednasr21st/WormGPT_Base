import json
import os
from datetime import datetime, timedelta

class AuthManager:
    def __init__(self, db_file="database/worm_secure_db.json"):
        self.db_file = db_file
        # إنشاء المجلد والملف إذا لم يوجدا
        if not os.path.exists("database"):
            os.makedirs("database")
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w") as f:
                json.dump({}, f)

    def load_db(self):
        try:
            with open(self.db_file, "r") as f:
                return json.load(f)
        except:
            return {}

    def save_db(self, data):
        with open(self.db_file, "w") as f:
            json.dump(data, f, indent=4)

    def verify_serial(self, serial_key, fingerprint):
        db = self.load_db()
        now = datetime.now()
        
        # قائمة السيريالات الافتراضية (يمكنك نقلها للوحة المدير لاحقاً)
        VALID_KEYS = {"WORM-MASTER-2026": 365, "VIP-HACKER-99": 30}

        if serial_key in VALID_KEYS:
            if serial_key not in db:
                # تفعيل السيريال لأول مرة
                db[serial_key] = {
                    "device_id": fingerprint,
                    "expiry": (now + timedelta(days=VALID_KEYS[serial_key])).strftime("%Y-%m-%d %H:%M:%S")
                }
                self.save_db(db)
                return True, "SUCCESS"
            else:
                user_info = db[serial_key]
                expiry = datetime.strptime(user_info["expiry"], "%Y-%m-%d %H:%M:%S")
                
                if now > expiry:
                    return False, "EXPIRED"
                if user_info["device_id"] != fingerprint:
                    return False, "LOCKED_TO_OTHER_DEVICE"
                
                return True, "SUCCESS"
        
        return False, "INVALID_KEY"
