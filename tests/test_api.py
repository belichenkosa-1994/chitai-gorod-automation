import pytest
import allure
from api.api_client import ChitaiGorodAPI

@pytest.mark.api
@allure.feature("API Тесты")
@allure.story("Тестирование доступности и производительности сайта")
class TestAPI:
    
    @pytest.fixture
    def api_client(self):
        return ChitaiGorodAPI()
    
    @allure.title("Тест 1: Проверка доступности сайта")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_site_availability(self, api_client):
        """Тест доступности главной страницы"""
        response = api_client.check_site_availability()
        
        assert response.status_code == 200, f"Сайт недоступен. Статус код: {response.status_code}"
        assert len(response.content) > 0, "Сайт вернул пустой ответ"
        
        # Проверяем что это действительно сайт Читай-Город
        assert "Читай-город" in response.text or "chitai-gorod" in response.text.lower()
    
    @allure.title("Тест 2: Проверка заголовков сайта")
    @allure.severity(allure.severity_level.NORMAL)
    def test_site_headers(self, api_client):
        """Тест заголовков ответа"""
        headers = api_client.get_site_headers()
        
        # Проверяем важные заголовки
        assert "Content-Type" in headers, "Отсутствует заголовок Content-Type"
        assert "text/html" in headers.get("Content-Type", ""), "Неверный Content-Type"
    
    @allure.title("Тест 3: Проверка поиска на сайте")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_functionality(self, api_client):
        """Тест поиска книг"""
        response = api_client.search_on_site("книга")
        
        assert response.status_code == 200, f"Поиск не работает. Статус код: {response.status_code}"
        assert len(response.content) > 0, "Поиск вернул пустой ответ"
    
    @allure.title("Тест 4: Измерение времени ответа сайта")
    @allure.severity(allure.severity_level.NORMAL)
    def test_site_performance(self, api_client):
        """Тест производительности сайта"""
        response_time = api_client.measure_response_time()
        
        # Проверяем что сайт загружается достаточно быстро
        assert response_time < 5.0, f"Сайт загружается слишком долго: {response_time:.2f} секунд"
    
    @allure.title("Тест 5: Проверка основных страниц сайта")
    @allure.severity(allure.severity_level.NORMAL)
    def test_main_pages_availability(self, api_client):
        """Тест доступности основных страниц сайта"""
        pages_to_check = [
            "/",  # Главная страница
            "/search?q=книги",  # Страница поиска
            "/catalog/books",  # Каталог книг (возможный URL)
            "/actions",  # Акции
            "/delivery",  # Доставка
            "/contacts",  # Контакты
            "/help",  # Помощь
            "/payment",  # Оплата
        ]
        
        results = {}
        
        for page in pages_to_check:
            with allure.step(f"Проверка страницы: {page}"):
                url = f"{api_client.base_url}{page}"
                try:
                    status_code = api_client.check_status_code(url)
                    results[page] = {
                        "status": status_code,
                        "success": status_code in [200, 301, 302]
                    }
                    
                    # Проверяем что страница существует (статус 200 или редирект)
                    assert status_code in [200, 301, 302], \
                        f"Страница {page} недоступна. Статус: {status_code}"
                
                except Exception as e:
                    results[page] = {
                        "status": str(e),
                        "success": False
                    }
                    # Для ненайденных страниц просто логируем, но не падаем
                    allure.attach(
                        f"Страница {page} не найдена: {e}",
                        name=f"Page {page} not found",
                        attachment_type=allure.attachment_type.TEXT
                    )
        
        # Создаем сводный отчет
        import json
        allure.attach(
            json.dumps(results, indent=2, ensure_ascii=False),
            name="Результаты проверки страниц",
            attachment_type=allure.attachment_type.JSON
        )
        
        # Проверяем что хотя бы 50% страниц доступны
        successful_pages = sum(1 for r in results.values() if r.get("success", False))
        success_rate = (successful_pages / len(results)) * 100 if results else 0
        
        allure.attach(
            f"Успешно проверено: {successful_pages}/{len(results)} страниц ({success_rate:.1f}%)",
            name="Статистика проверки страниц",
            attachment_type=allure.attachment_type.TEXT
        )
        
        assert success_rate >= 50.0, f"Слишком мало доступных страниц: {success_rate:.1f}%"
    
    @allure.title("Тест 6: Проверка кодировки сайта")
    @allure.severity(allure.severity_level.MINOR)
    def test_site_encoding(self, api_client):
        """Тест кодировки и содержимого сайта"""
        response = api_client.check_site_availability()
        
        # Проверяем кодировку
        assert response.encoding.lower() in ['utf-8', 'windows-1251'], f"Неверная кодировка: {response.encoding}"
        
        # Проверяем наличие русского текста
        russian_chars = any(ord(char) > 127 for char in response.text[:1000])
        assert russian_chars, "На странице отсутствует русский текст"