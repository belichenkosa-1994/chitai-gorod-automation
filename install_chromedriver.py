import os
import sys
import zipfile
import requests
from bs4 import BeautifulSoup
import re

def get_chrome_version():
    """Получить версию Chrome"""
    import winreg
    
    try:
        # Путь к реестру Chrome
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
        
        # Открываем реестр
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ)
        
        # Получаем путь к Chrome
        chrome_path, _ = winreg.QueryValueEx(reg_key, None)
        winreg.CloseKey(reg_key)
        
        # Получаем версию из файла
        import subprocess
        result = subprocess.run([chrome_path, '--version'], capture_output=True, text=True, shell=True)
        version = result.stdout.strip().split()[-1]
        
        return version
    except Exception as e:
        print(f"Не удалось получить версию Chrome: {e}")
        return None

def download_chromedriver(version):
    """Скачать ChromeDriver"""
    # Основной URL для скачивания
    base_url = "https://chromedriver.storage.googleapis.com"
    
    # Получаем список доступных версий
    list_url = f"{base_url}/"
    response = requests.get(list_url)
    
    if response.status_code != 200:
        print("Не удалось получить список версий ChromeDriver")
        return False
    
    # Парсим XML ответ
    soup = BeautifulSoup(response.content, 'xml')
    
    # Ищем ключи (версии)
    keys = soup.find_all('Key')
    
    # Фильтруем по версии и платформе
    pattern = re.compile(f"{version}\.\d+\.\d+\.\d+/chromedriver_win32\.zip")
    matching_keys = [key.text for key in keys if pattern.match(key.text)]
    
    if not matching_keys:
        print(f"Не найдена версия ChromeDriver для Chrome {version}")
        # Пробуем найти ближайшую версию
        print("Ищем ближайшую версию...")
        version_prefix = version.split('.')[0]  # Берем мажорную версию
        pattern2 = re.compile(f"{version_prefix}\.\d+\.\d+\.\d+/chromedriver_win32\.zip")
        matching_keys = [key.text for key in keys if pattern2.match(key.text)]
        
        if not matching_keys:
            print("Не найдено подходящих версий")
            return False
        
        # Берем последнюю версию
        latest_key = sorted(matching_keys)[-1]
        version = latest_key.split('/')[0]
        print(f"Используем версию: {version}")
    else:
        latest_key = sorted(matching_keys)[-1]
        version = latest_key.split('/')[0]
    
    # Скачиваем ChromeDriver
    download_url = f"{base_url}/{version}/chromedriver_win32.zip"
    print(f"Скачиваем ChromeDriver {version}...")
    
    response = requests.get(download_url)
    if response.status_code != 200:
        print(f"Ошибка скачивания: {response.status_code}")
        return False
    
    # Сохраняем ZIP файл
    zip_path = "chromedriver_win32.zip"
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    
    # Распаковываем
    print("Распаковываем...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall()
    
    # Удаляем ZIP файл
    os.remove(zip_path)
    
    # Проверяем что файл создан
    if os.path.exists("chromedriver.exe"):
        print("ChromeDriver успешно установлен!")
        return True
    else:
        print("ChromeDriver не найден после распаковки")
        return False

def main():
    """Основная функция"""
    print("=" * 50)
    print("Установка ChromeDriver для Selenium")
    print("=" * 50)
    
    # Получаем версию Chrome
    chrome_version = get_chrome_version()
    
    if chrome_version:
        print(f"Установленная версия Chrome: {chrome_version}")
        
        # Скачиваем ChromeDriver
        if download_chromedriver(chrome_version):
            print("\nChromeDriver успешно установлен!")
            print("Можно запускать UI тесты.")
        else:
            print("\nНе удалось установить ChromeDriver.")
            print("Попробуйте установить вручную:")
            print("1. Откройте https://chromedriver.chromium.org/")
            print("2. Скачайте версию, соответствующую вашему Chrome")
            print("3. Положите chromedriver.exe в папку с проектом")
    else:
        print("Chrome не найден или не установлен.")
        print("Установите Google Chrome и повторите попытку.")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()