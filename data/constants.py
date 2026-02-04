class SiteConstants:
    """Константы сайта Читай-Город"""
    
    # Таймауты
    SEARCH_TIMEOUT = 10
    PAGE_LOAD_TIMEOUT = 30
    ELEMENT_TIMEOUT = 10
    
    # Ожидаемые тексты
    SEARCH_NO_RESULTS_TEXT = "К сожалению, по вашему запросу ничего не найдено"
    CART_EMPTY_TEXT = "Ваша корзина пуста"
    AUTH_ERROR_TEXT = "Неверный код"
    
    # CSS классы
    BUTTON_PRIMARY_CLASS = "button--primary"
    BUTTON_SECONDARY_CLASS = "button--secondary"
    
    # Атрибуты data-testid (предполагаемые)
    SEARCH_INPUT_TESTID = "search-input"
    SEARCH_BUTTON_TESTID = "search-button"
    CART_ICON_TESTID = "cart-icon"
    LOGIN_BUTTON_TESTID = "login-button"