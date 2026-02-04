import random
import string
import time
from typing import Any, Dict
import allure

def generate_random_email() -> str:
    """Сгенерировать случайный email для тестов"""
    random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"test_{random_string}@example.com"

def generate_random_phone() -> str:
    """Сгенерировать случайный номер телефона"""
    return f"+7{random.randint(900, 999)}{random.randint(1000000, 9999999)}"

def measure_execution_time(func):
    """Декоратор для измерения времени выполнения функции"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Логируем время выполнения
        allure.attach(
            f"Функция: {func.__name__}\n"
            f"Время выполнения: {execution_time:.2f} секунд",
            name="Время выполнения функции",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return result
    return wrapper

def wait_for_condition(condition_func, timeout: int = 10, interval: float = 0.5):
    """Ожидание выполнения условия"""
    end_time = time.time() + timeout
    
    while time.time() < end_time:
        if condition_func():
            return True
        time.sleep(interval)
    
    return False