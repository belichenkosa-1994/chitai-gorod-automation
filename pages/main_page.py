from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import allure
from .base_page import BasePage
import time

class MainPage(BasePage):
    """Page Object для главной страницы Читай-Город"""
    
    # АКТУАЛЬНЫЕ локаторы для реального сайта chitai-gorod.ru
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[data-test-id='search-input'], input.search-field__input, input[name='q'], input[placeholder*='поиск']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[data-test-id='search-button'], button.search-field__button, button[type='submit']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "a[data-test-id='login-button'], a.header-login__link, a[href*='login'], button[data-test-id='header-login-button']")
    CART_ICON = (By.CSS_SELECTOR, "a[data-test-id='cart-button'], a.header-cart__link, a[href*='cart']")
    CATEGORIES_MENU = (By.CSS_SELECTOR, "button[data-test-id='catalog-button'], button.catalog-button")
    COOKIES_ACCEPT = (By.CSS_SELECTOR, "button.cookie-warning__button, button[data-test-id='cookie-accept']")
    
    # Дополнительные элементы для проверки
    LOGO = (By.CSS_SELECTOR, "a[data-test-id='logo'], a.header-logo")
    HEADER = (By.CSS_SELECTOR, "header[data-test-id='header'], header.header")
    FOOTER = (By.CSS_SELECTOR, "footer[data-test-id='footer'], footer.footer")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    @allure.step("Открыть главную страницу")
    def open_main_page(self) -> None:
        """Открыть главную страницу с обработкой куки"""
        self.open("/")
        time.sleep(3)  # Ждем загрузки
        
        # Пробуем принять куки если есть
        try:
            self.accept_cookies()
        except:
            pass  # Если окна куки нет, пропускаем
    
    @allure.step("Принять куки")
    def accept_cookies(self) -> None:
        """Принять уведомление о куки если оно есть"""
        if self.is_element_visible(self.COOKIES_ACCEPT, timeout=5):
            self.click(self.COOKIES_ACCEPT)
            time.sleep(1)
    
    @allure.step("Выполнить поиск: {query}")
    def search_book(self, query: str) -> None:
        """Выполнить поиск книги с ожиданием"""
        # Ждем пока поле поиска станет видимым
        self.wait_for_element_visible(self.SEARCH_INPUT)
        
        # Вводим текст
        self.type_text(self.SEARCH_INPUT, query)
        
        # Кликаем кнопку поиска
        time.sleep(1)  # Небольшая задержка
        self.click(self.SEARCH_BUTTON)
        
        # Ждем загрузки результатов
        time.sleep(3)
    
    @allure.step("Перейти в корзину")
    def go_to_cart(self) -> None:
        """Перейти в корзину"""
        self.click(self.CART_ICON)
        time.sleep(2)  # Ждем загрузки корзины
    
    @allure.step("Перейти на страницу авторизации")
    def go_to_login(self) -> None:
        """Перейти на страницу авторизации"""
        self.click(self.LOGIN_BUTTON)
        time.sleep(2)  # Ждем загрузки формы авторизации
    
    @allure.step("Проверить отображение поискового поля")
    def is_search_displayed(self) -> bool:
        """Проверить видимость поискового поля"""
        return self.is_element_visible(self.SEARCH_INPUT, timeout=10)
    
    @allure.step("Проверить отображение основных элементов")
    def check_basic_elements(self) -> dict:
        """Проверить наличие основных элементов на странице"""
        elements = {
            "Логотип": self.is_element_visible(self.LOGO, timeout=5),
            "Поиск": self.is_element_visible(self.SEARCH_INPUT, timeout=5),
            "Корзина": self.is_element_visible(self.CART_ICON, timeout=5),
            "Шапка": self.is_element_visible(self.HEADER, timeout=5),
            "Подвал": self.is_element_visible(self.FOOTER, timeout=5),
        }
        return elements
    
    @allure.step("Дождаться видимости элемента")
    def wait_for_element_visible(self, locator, timeout: int = 10):
        """Дождаться видимости элемента"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))