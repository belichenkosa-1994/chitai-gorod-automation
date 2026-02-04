import os
from dotenv import load_dotenv

load_dotenv()

class Credentials:
    """Учетные данные (вынесены в отдельный файл)"""
    TEST_EMAIL = os.getenv("TEST_USER_EMAIL", "test@example.com")
    TEST_PASSWORD = os.getenv("TEST_USER_PASSWORD", "password123")
    TEST_PHONE = os.getenv("TEST_USER_PHONE", "+79991234567")