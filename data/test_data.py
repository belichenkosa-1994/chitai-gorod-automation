from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Book:
    """Данные книги"""
    title: str
    author: str
    isbn: str
    category: str

class TestData:
    """Тестовые данные для сайта Читай-Город"""
    
    # Тестовые книги
    BOOKS = [
        Book(
            title="Мастер и Маргарита",
            author="Михаил Булгаков",
            isbn="978-5-17-090644-2",
            category="Русская классика"
        ),
        Book(
            title="1984",
            author="Джордж Оруэлл",
            isbn="978-5-17-090987-0",
            category="Зарубежная классика"
        ),
        Book(
            title="Психология влияния",
            author="Роберт Чалдини",
            isbn="978-5-496-01187-3",
            category="Психология"
        )
    ]
    
    # Поисковые запросы
    SEARCH_QUERIES = {
        "valid": ["Психология", "Булгаков", "программирование"],
        "invalid": ["asdfghjkl12345", "несуществующаякнига123"],
        "partial": ["псих", "булг", "prog"]
    }
    
    # URL страниц
    URLS = {
        "main": "/",
        "search": "/search",
        "cart": "/cart",
        "auth": "/auth"
    }