import requests
import allure
import json
from typing import Dict, Any, Optional
from datetime import datetime
from config.config import config

class ChitaiGorodAPI:
    """API клиент для тестирования сайта Читай-Город"""
    
    def __init__(self):
        self.base_url = config.base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
        })
        # Устанавливаем timeout
        self.timeout = 10
    
    @allure.step("Проверить доступность сайта")
    def check_site_availability(self) -> requests.Response:
        """Проверить доступность главной страницы"""
        return self.session.get(self.base_url, timeout=self.timeout)
    
    @allure.step("Получить заголовки сайта")
    def get_site_headers(self) -> Dict:
        """Получить заголовки ответа"""
        response = self.session.head(self.base_url, timeout=self.timeout)
        return dict(response.headers)
    
    @allure.step("Поиск книги на сайте: {query}")
    def search_on_site(self, query: str) -> requests.Response:
        """Поиск книги через поисковую форму сайта"""
        # Получаем главную страницу чтобы получить CSRF токен если нужно
        response = self.session.get(self.base_url, timeout=self.timeout)
        
        # Ищем форму поиска - обычно это GET запрос с параметром q
        search_url = f"{self.base_url}/search"
        params = {"q": query}
        
        return self.session.get(search_url, params=params, timeout=self.timeout)
    
    @allure.step("Получить страницу категории: {category}")
    def get_category_page(self, category: str) -> requests.Response:
        """Получить страницу категории"""
        # Формируем URL категории (зависит от структуры сайта)
        category_url = f"{self.base_url}/catalog/{category}"
        return self.session.get(category_url, timeout=self.timeout)
    
    @allure.step("Измерить время ответа сайта")
    def measure_response_time(self, url: str = None) -> float:
        """Измерить время ответа сайта"""
        if url is None:
            url = self.base_url
        
        start_time = datetime.now()
        response = self.session.get(url, timeout=self.timeout)
        end_time = datetime.now()
        
        response_time = (end_time - start_time).total_seconds()
        
        # Логируем для Allure
        allure.attach(
            f"URL: {url}\n"
            f"Время ответа: {response_time:.2f} секунд\n"
            f"Статус код: {response.status_code}\n"
            f"Размер ответа: {len(response.content)} байт",
            name="Метрики производительности сайта",
            attachment_type=allure.attachment_type.TEXT
        )
        
        return response_time
    
    @allure.step("Проверить статус код страницы")
    def check_status_code(self, url: str) -> int:
        """Проверить статус код страницы"""
        response = self.session.get(url, timeout=self.timeout)
        return response.status_code
    
    def _log_response(self, response: requests.Response) -> None:
        """Логировать ответ"""
        allure.attach(
            f"URL: {response.url}\n"
            f"Статус: {response.status_code}\n"
            f"Заголовки: {dict(response.headers)}",
            name="Детали ответа",
            attachment_type=allure.attachment_type.TEXT
        )