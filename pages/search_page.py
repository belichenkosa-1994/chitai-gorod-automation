from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import allure
from .base_page import BasePage  # Относительный импорт внутри pages
from data.constants import SiteConstants  # Абсолютный импорт из data

class SearchPage(BasePage):
    """Page Object для страницы поиска"""
    
    # Локаторы страницы поиска
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".search-results, .product-list, .books-list, .catalog-grid")
    NO_RESULTS_MESSAGE = (By.XPATH, f"//*[contains(text(), '{SiteConstants.SEARCH_NO_RESULTS_TEXT}')]")
    BOOK_TITLES = (By.CSS_SELECTOR, ".product-title, .book-title, .item-title")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".buy-button, .add-to-cart, [data-action='add-to-cart']")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    @allure.step("Проверить наличие результатов поиска")
    def has_search_results(self) -> bool:
        """Проверить есть ли результаты поиска"""
        return self.is_element_visible(self.SEARCH_RESULTS, timeout=10)
    
    @allure.step("Проверить сообщение 'ничего не найдено'")
    def is_no_results_message_displayed(self) -> bool:
        """Проверить отображение сообщения об отсутствии результатов"""
        return self.is_element_visible(self.NO_RESULTS_MESSAGE, timeout=5)
    
    @allure.step("Получить количество найденных книг")
    def get_results_count(self) -> int:
        """Получить количество найденных книг"""
        try:
            elements = self.find_elements(self.BOOK_TITLES, timeout=5)
            return len(elements)
        except:
            return 0
    
    @allure.step("Добавить первую книгу в корзину")
    def add_first_book_to_cart(self) -> str:
        """Добавить первую книгу в корзину и вернуть ее название"""
        book_titles = self.find_elements(self.BOOK_TITLES)
        if not book_titles:
            raise ValueError("На странице нет книг")
        
        book_name = book_titles[0].text
        
        add_buttons = self.find_elements(self.ADD_TO_CART_BUTTON)
        if add_buttons:
            add_buttons[0].click()
        
        return book_name