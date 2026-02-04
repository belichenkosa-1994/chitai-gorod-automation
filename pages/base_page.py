from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from typing import List, Tuple, Optional
import allure
import time
from config.config import config

class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.timeout)
        self.base_url = config.base_url
    
    @allure.step("Открыть страницу {url}")
    def open(self, url: str = "") -> None:
        """Открыть страницу"""
        full_url = f"{self.base_url}{url}"
        try:
            self.driver.get(full_url)
            # Ждем загрузки страницы
            time.sleep(2)
        except Exception as e:
            allure.attach(f"Ошибка при открытии {full_url}: {str(e)}", 
                         name="Page Load Error", 
                         attachment_type=allure.attachment_type.TEXT)
            raise
    
    @allure.step("Найти элемент {locator}")
    def find_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Найти элемент с ожиданием (более надежная версия)"""
        wait = WebDriverWait(self.driver, timeout or config.timeout)
        
        # Пробуем разные стратегии поиска
        try:
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            # Пробуем найти по видимости
            try:
                return wait.until(EC.visibility_of_element_located(locator))
            except TimeoutException:
                # Пробуем найти вообще любой элемент
                elements = self.driver.find_elements(*locator)
                if elements:
                    return elements[0]
                else:
                    raise
    
    @allure.step("Найти элементы {locator}")
    def find_elements(self, locator: Tuple[str, str], timeout: int = None) -> List[WebElement]:
        """Найти несколько элементов"""
        try:
            wait = WebDriverWait(self.driver, timeout or config.timeout)
            return wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            # Возвращаем пустой список если не нашли
            return []
    
    @allure.step("Кликнуть на элемент {locator}")
    def click(self, locator: Tuple[str, str]) -> None:
        """Кликнуть на элемент с повторными попытками"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                element = self.find_element(locator)
                element.click()
                return
            except (StaleElementReferenceException, NoSuchElementException) as e:
                if attempt == max_attempts - 1:
                    raise
                time.sleep(1)
    
    @allure.step("Ввести текст '{text}' в элемент {locator}")
    def type_text(self, locator: Tuple[str, str], text: str) -> None:
        """Ввести текст в поле"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator: Tuple[str, str]) -> str:
        """Получить текст элемента"""
        return self.find_element(locator).text
    
    @allure.step("Проверить видимость элемента {locator}")
    def is_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Проверить видимость элемента"""
        try:
            wait = WebDriverWait(self.driver, timeout or config.timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    @allure.step("Сделать скриншот")
    def take_screenshot(self, name: str = "screenshot") -> None:
        """Сделать скриншот и прикрепить к Allure"""
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )