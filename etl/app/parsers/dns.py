import sys
import json
import random
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

"""Прочитай описание в файле intruction_get_price.md"""

# Константы
PRICE_SELECTOR = '.product-buy__price'
WAIT_TIMEOUT = 60000
DEBUG_HTML_FILE = 'debug_page.html' # Сохраняю еще страницу, чтобы чекать ошибки или находить селекторы

def _create_browser_context(profile_path, headless=True):
    """Запускаем браузер с искусственным профилем"""
    playwright = sync_playwright().start()
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=profile_path,
        headless=headless,
        args=['--disable-blink-features=AutomationControlled']
        # В args можно много параметров передавать, также можно сделать так чтобы браузер считал
        # что у нас открыто окно но headless=true, но чет не работало
    )
    return playwright, context

def _emulate_human_behavior(page):
    """Имитирует движения мыши и скролл для обхода защиты"""
    page.mouse.move(random.randint(100, 500), random.randint(100, 500))
    page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.3);")
    page.wait_for_timeout(2000)

def _extract_price_from_page(html):
    """
    Извлекает цену из HTML страницы.
    Сначала пробует JSON, затем ищет элемент с классом product-buy__price.
    Возвращает float или None.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # JSON
    script = soup.find('script', type='application/ld+json')
    if script:
        try:
            data = json.loads(script.string)
            if 'offers' in data:
                price = data['offers'].get('price')
                if price:
                    print(f"Цена из JSON-LD: {price}")
                    return float(price)
        except Exception as e:
            print(f"Ошибка парсинга JSON: {e}")

    # HTML элемент
    price_elem = soup.find(class_='product-buy__price')
    if price_elem:
        price_text = price_elem.get_text(strip=True)
        print(f"Найден элемент с классом product-buy__price: {price_text}")
        price_clean = price_text.replace('\xa0', ' ').replace('₽', '').strip().replace(' ', '')
        try:
            return float(price_clean)
        except:
            pass
    return None

def _save_debug_page(html):
    """Сохраняет HTML в файл для отладки."""
    with open(DEBUG_HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Страница сохранена в {DEBUG_HTML_FILE} для анализа")

def fetch_price_from_url(url, profile_path='./chrome_profile', headless=True):
    """
    Получает цену товара со страницы DNS.

    :param url: ссылка на товар
    :param profile_path: путь к папке с профилем браузера
    :param headless: запускать браузер в фоновом режиме (True) или с окном (False)
    :return цена товара (float)
    """
    playwright = None
    context = None
    try:
        playwright, context = _create_browser_context(profile_path, headless)
        page = context.new_page()

        print("Переход на страницу...")
        page.goto(url, wait_until='networkidle', timeout=WAIT_TIMEOUT)

        # Ждём загрузку динамического контента
        page.wait_for_timeout(3000)

        # Имитация человеческого поведения
        _emulate_human_behavior(page)

        # Проверяем наличие цены
        price_element = page.locator(PRICE_SELECTOR).first
        if price_element.count() > 0:
            print(f"Найден элемент с ценой: {price_element.text_content()}")

        html = page.content()
        price = _extract_price_from_page(html)

        if price is None:
            _save_debug_page(html)
            raise ValueError("Цена не найдена на странице")

        return price

    finally:
        if context:
            context.close()
        if playwright:
            playwright.stop()


def run():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Введите ссылку на товар DNS: ").strip()

    try:
        price = fetch_price_from_url(url, headless=False)  # можно изменить на False для отладки
        print(f"Цена товара: {price} ₽")
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    run()
