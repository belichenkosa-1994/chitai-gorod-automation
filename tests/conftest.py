import pytest
import allure
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from config.config import config
from config.ui_config import BrowserConfig
from api.api_client import ChitaiGorodAPI

@pytest.fixture(scope="session")
def api_client():
    """Фикстура для API клиента"""
    client = ChitaiGorodAPI()
    yield client
    client.session.close()

import pytest
import allure
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from config.config import config

@pytest.fixture(scope="function")
def driver():
    """Упрощенная фикстура драйвера"""
    driver = None
    
    try:
        if config.browser.lower() == "chrome":
            # Простые настройки Chrome
            options = ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument(f"--window-size={config.window_width},{config.window_height}")
            
            if config.headless:
                options.add_argument("--headless")
            
            # Пробуем несколько способов
            try:
                # Способ 1: Через webdriver-manager
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except:
                # Способ 2: Прямой путь к chromedriver
                chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
                if os.path.exists(chromedriver_path):
                    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
                else:
                    # Способ 3: Без service
                    driver = webdriver.Chrome(options=options)
        
        elif config.browser.lower() == "firefox":
            # Настройки Firefox
            options = FirefoxOptions()
            
            if config.headless:
                options.add_argument("--headless")
            
            options.add_argument(f"--width={config.window_width}")
            options.add_argument(f"--height={config.window_height}")
            
            try:
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)
            except:
                driver = webdriver.Firefox(options=options)
        
        else:
            pytest.skip(f"Браузер {config.browser} не поддерживается")
    
    except Exception as e:
        print(f"Ошибка создания драйвера: {e}")
        # Попробуем создать драйвер самым простым способом
        try:
            if config.browser.lower() == "chrome":
                driver = webdriver.Chrome()
            elif config.browser.lower() == "firefox":
                driver = webdriver.Firefox()
        except Exception as e2:
            print(f"Не удалось создать драйвер: {e2}")
            pytest.skip(f"Не удалось запустить браузер: {e2}")
    
    if driver is None:
        pytest.skip("Драйвер не создан")
    
    # Настройки
    driver.set_window_size(config.window_width, config.window_height)
    driver.implicitly_wait(config.timeout)
    
    yield driver
    
    # Закрытие
    if driver:
        try:
            driver.quit()
        except:
            pass

# Обновляем хук для скриншотов
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            if 'driver' in item.fixturenames:
                driver = item.funcargs.get('driver')
                if driver:
                    screenshot = driver.get_screenshot_as_png()
                    allure.attach(
                        screenshot,
                        name="screenshot_on_failure",
                        attachment_type=allure.attachment_type.PNG
                    )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")