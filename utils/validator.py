import re

class Validator:
    @staticmethod
    def validate_email(email):
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

    @staticmethod
    def validate_phone(phone):
        return phone.isdigit() and len(phone) == 11  # 假设是11位数字手机号

    @staticmethod
    def validate_non_empty(value):
        return bool(value.strip())
