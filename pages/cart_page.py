from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import allure
from .base_page import BasePage  # Относительный внутри pages
from data.constants import SiteConstants  # Абсолютный импорт

class CartPage(BasePage):
    """Page Object для страницы корзины"""
    
    # Локаторы корзины
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item, .basket-item, .order-item")
    CART_EMPTY_MESSAGE = (By.XPATH, f"//*[contains(text(), '{SiteConstants.CART_EMPTY_TEXT}')]")
    ITEM_TITLE = (By.CSS_SELECTOR, ".item-title, .product-name, .book-title")
    REMOVE_BUTTON = (By.CSS_SELECTOR, ".remove-item, .delete-item, [data-action='remove']")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".total-price, .order-total, .sum")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    @allure.step("Проверить пуста ли корзина")
    def is_cart_empty(self) -> bool:
        """Проверить пуста ли корзина"""
        return self.is_element_visible(self.CART_EMPTY_MESSAGE, timeout=5)
    
    @allure.step("Получить список товаров в корзине")
    def get_cart_items(self) -> list:
        """Получить список названий товаров в корзине"""
        try:
            items = self.find_elements(self.ITEM_TITLE, timeout=5)
            return [item.text for item in items]
        except:
            return []
    
    @allure.step("Получить количество товаров в корзине")
    def get_items_count(self) -> int:
        """Получить количество товаров в корзине"""
        return len(self.get_cart_items())
    
    @allure.step("Удалить первый товар из корзины")
    def remove_first_item(self) -> None:
        """Удалить первый товар из корзины"""
        remove_buttons = self.find_elements(self.REMOVE_BUTTON)
        if remove_buttons:
            remove_buttons[0].click()
            # Подтверждение удаления если нужно
            self.driver.switch_to.alert.accept() if self.is_alert_present() else None
    
    def is_alert_present(self) -> bool:
        """Проверить наличие alert"""
        try:
            self.driver.switch_to.alert
            return True
        except:
            return False