import sys
import io
import contextlib
import traceback

class CodeExecutor:
    def __init__(self):
        pass

    def execute_python(self, code_string):
        """
        تنفيذ كود بايثون والتقاط المخرجات (stdout)
        """
        # إنشاء "مصب" لالتقاط المخرجات النصية
        output_capture = io.StringIO()
        
        try:
            # توجيه المخرجات من الشاشة إلى الكائن الخاص بنا
            with contextlib.redirect_stdout(output_capture):
                # تنفيذ الكود في بيئة محلية
                # ملاحظة: exec تستخدم بحذر، ولكنها هنا جزء من وظيفة الهاكر-بوت
                exec(code_string, {'__builtins__': __builtins__}, {})
            
            result = output_capture.getvalue()
            if not result:
                result = "Code executed successfully (No output returned)."
            return result, "SUCCESS"

        except Exception:
            # في حال حدوث خطأ، نقوم بطباعة تفاصيل الخطأ (Traceback)
            error_msg = traceback.format_exc()
            return error_msg, "ERROR"

    def format_executor_response(self, code_result, status):
        """
        تنسيق النتيجة لتظهر بشكل احترافي في الشات
        """
        if status == "SUCCESS":
            return (
                f"✅ **Execution Successful**\n"
                f"```text\n{code_result}\n```"
            )
        else:
            return (
                f"❌ **Execution Failed (Debug Info)**\n"
                f"```python\n{code_result}\n```"
            )
