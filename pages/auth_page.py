from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import allure
from .base_page import BasePage  # Относительный внутри pages
import time

class AuthPage(BasePage):
    """Page Object для страницы авторизации"""
    
    # Локаторы авторизации
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email'], input[name='email']")
    PHONE_INPUT = (By.CSS_SELECTOR, "input[type='tel'], input[name='phone']")
    CODE_INPUT = (By.CSS_SELECTOR, "input[type='text'][maxlength='6'], input[name='code']")
    SEND_CODE_BUTTON = (By.XPATH, "//button[contains(text(), 'Получить код') or contains(text(), 'Отправить код')]")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти') or contains(text(), 'Продолжить')]")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message, .alert-error, .notification-error")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    @allure.step("Авторизация по email {email}")
    def login_by_email(self, email: str, code: str = "000000") -> bool:
        """Авторизация по email"""
        try:
            # Вводим email
            self.type_text(self.EMAIL_INPUT, email)
            
            # Нажимаем кнопку получения кода
            if self.is_element_visible(self.SEND_CODE_BUTTON, timeout=5):
                self.click(self.SEND_CODE_BUTTON)
                time.sleep(2)  # Ждем отправки кода
            
            # Вводим код (в тестах используем заглушку)
            if self.is_element_visible(self.CODE_INPUT, timeout=5):
                self.type_text(self.CODE_INPUT, code)
            
            # Нажимаем кнопку входа
            if self.is_element_visible(self.SUBMIT_BUTTON, timeout=5):
                self.click(self.SUBMIT_BUTTON)
                time.sleep(3)  # Ждем обработки
            
            return "auth" not in self.driver.current_url
        except Exception as e:
            allure.attach(f"Ошибка авторизации: {str(e)}", name="Auth Error", attachment_type=allure.attachment_type.TEXT)
            return False
    
    @allure.step("Проверить наличие ошибки авторизации")
    def is_error_displayed(self) -> bool:
        """Проверить отображение ошибки"""
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=5)