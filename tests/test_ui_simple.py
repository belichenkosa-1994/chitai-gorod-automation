#упрощенная версия тестов
import pytest
import allure
import time
from selenium.webdriver.common.by import By

@pytest.mark.ui
@allure.feature("UI Тесты (упрощенные)")
class TestUISimple:
    
    @allure.title("Тест 1: Загрузка главной страницы")
    def test_load_main_page(self, driver):
        """Проверка что главная страница загружается"""
        driver.get("https://www.chitai-gorod.ru")
        time.sleep(3)  # Даем время на загрузку
        
        # Делаем скриншот
        allure.attach(
            driver.get_screenshot_as_png(),
            name="main_page",
            attachment_type=allure.attachment_type.PNG
        )
        
        # Базовые проверки
        assert "chitai-gorod" in driver.current_url
        assert driver.title
        assert len(driver.page_source) > 10000
    
    @allure.title("Тест 2: Наличие русского текста")
    def test_russian_text(self, driver):
        """Проверка что на странице есть русский текст"""
        driver.get("https://www.chitai-gorod.ru")
        time.sleep(2)
        
        # Получаем текст страницы
        page_text = driver.page_source
        
        # Проверяем наличие русских букв
        russian_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        found_russian = any(letter in page_text.lower() for letter in russian_letters)
        
        assert found_russian, "Русский текст не найден на странице"
    
    @allure.title("Тест 3: Проверка заголовка страницы")
    def test_page_title(self, driver):
        """Проверка заголовка страницы"""
        driver.get("https://www.chitai-gorod.ru")
        time.sleep(2)
        
        title = driver.title
        allure.attach(f"Заголовок страницы: {title}", 
                     name="Page Title", 
                     attachment_type=allure.attachment_type.TEXT)
        
        # Проверяем что заголовок не пустой и достаточно длинный
        assert title
        assert len(title) > 10
    
    @allure.title("Тест 4: Проверка навигации")
    def test_navigation(self, driver):
        """Проверка что можно перейти по ссылкам"""
        driver.get("https://www.chitai-gorod.ru")
        time.sleep(2)
        
        # Ищем все ссылки
        links = driver.find_elements(By.TAG_NAME, "a")
        
        # Проверяем что есть ссылки
        assert len(links) > 10, f"Найдено только {len(links)} ссылок"
        
        # Логируем несколько ссылок
        sample_links = [link.get_attribute("href") for link in links[:5] if link.get_attribute("href")]
        allure.attach("\n".join(sample_links), 
                     name="Sample Links", 
                     attachment_type=allure.attachment_type.TEXT)
    
    @allure.title("Тест 5: Проверка времени ответа")
    def test_response_time(self, driver):
        """Проверка времени загрузки страницы"""
        start_time = time.time()
        driver.get("https://www.chitai-gorod.ru")
        
        # Ждем пока страница загрузится
        driver.implicitly_wait(10)
        
        end_time = time.time()
        load_time = end_time - start_time
        
        allure.attach(f"Время загрузки: {load_time:.2f} секунд", 
                     name="Load Time", 
                     attachment_type=allure.attachment_type.TEXT)
        
        assert load_time < 15.0, f"Страница загружается слишком долго: {load_time:.2f}с"
    
    @allure.title("Тест 6: Проверка элементов страницы")
    def test_page_elements(self, driver):
        """Проверка наличия основных элементов"""
        driver.get("https://www.chitai-gorod.ru")
        time.sleep(2)
        
        elements_to_check = [
            ("Заголовок H1", By.TAG_NAME, "h1"),
            ("Навигация", By.TAG_NAME, "nav"),
            ("Изображения", By.TAG_NAME, "img"),
            ("Ссылки", By.TAG_NAME, "a"),
            ("Кнопки", By.TAG_NAME, "button"),
        ]
        
        results = []
        for name, by, value in elements_to_check:
            try:
                elements = driver.find_elements(by, value)
                found = len(elements) > 0
                results.append(f"{name}: {'✓' if found else '✗'} ({len(elements)} элементов)")
            except:
                results.append(f"{name}: ✗ (ошибка поиска)")
        
        allure.attach("\n".join(results), 
                     name="Elements Check", 
                     attachment_type=allure.attachment_type.TEXT)
        
        # Проверяем что найдено хотя бы 4 из 5 типов элементов
        found_count = sum(1 for r in results if "✓" in r)
        assert found_count >= 4, f"Найдено только {found_count} из 5 типов элементов"