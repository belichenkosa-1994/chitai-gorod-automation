import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Конфигурация проекта для Читай-Город"""
    base_url: str = os.getenv("BASE_URL", "https://www.chitai-gorod.ru")
    api_url: str = os.getenv("API_URL", "https://api.chitai-gorod.ru")
    
    # Настройки браузера
    browser: str = os.getenv("BROWSER", "chrome")
    headless: bool = os.getenv("HEADLESS", "false").lower() == "true"
    window_width: int = int(os.getenv("WINDOW_WIDTH", "1920"))
    window_height: int = int(os.getenv("WINDOW_HEIGHT", "1080"))
    timeout: int = int(os.getenv("TIMEOUT", "15"))
    
    # Настройки тестирования
    search_timeout: int = int(os.getenv("SEARCH_TIMEOUT", "30"))
    page_load_timeout: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "60"))
    
    # Критерии производительности (из баг-репорта)
    max_page_load_time: float = float(os.getenv("MAX_PAGE_LOAD_TIME", "5.0"))  # секунд
    
    # Режимы тестирования
    enable_performance_testing: bool = os.getenv("ENABLE_PERFORMANCE_TESTING", "true").lower() == "true"
    
    @property
    def is_production(self) -> bool:
        return "chitai-gorod.ru" in self.base_url

config = Config()