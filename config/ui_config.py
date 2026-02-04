from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# Абсолютный импорт
from config.config import config

class BrowserConfig:
    """Конфигурация браузера для UI тестов"""
    
    @staticmethod
    def get_chrome_options() -> ChromeOptions:
        """Получить настройки Chrome"""
        options = ChromeOptions()
        
        if config.headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--window-size={config.window_width},{config.window_height}")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        return options
    
    @staticmethod
    def get_firefox_options() -> FirefoxOptions:
        """Получить настройки Firefox"""
        options = FirefoxOptions()
        
        if config.headless:
            options.add_argument("--headless")
        
        options.add_argument(f"--width={config.window_width}")
        options.add_argument(f"--height={config.window_height}")
        
        return options