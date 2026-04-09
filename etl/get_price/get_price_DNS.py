import json
import random
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

PRICE_SELECTOR = '.product-buy__price'
WAIT_TIMEOUT = 60000
DEBUG_HTML_FILE = 'debug_page.html'

def _create_browser_context(profile_path, headless=False):
    playwright = sync_playwright().start()
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=profile_path,
        headless=headless,
        args=['--disable-blink-features=AutomationControlled']
    )
    return playwright, context

def _emulate_human_behavior(page):
    page.mouse.move(random.randint(100, 500), random.randint(100, 500))
    page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.3);")
    page.wait_for_timeout(2000)

def _extract_price_from_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    script = soup.find('script', type='application/ld+json')
    if script:
        try:
            data = json.loads(script.string)
            if 'offers' in data:
                price = data['offers'].get('price')
                if price:
                    return float(price), data.get('name')
        except Exception:
            pass

    price_elem = soup.find(class_='product-buy__price')
    if price_elem:
        price_text = price_elem.get_text(strip=True)
        price_clean = price_text.replace('\xa0', ' ').replace('₽', '').strip().replace(' ', '')
        try:
            return float(price_clean), soup.find('h1').get_text(strip=True) if soup.find('h1') else "Неизвестный товар"
        except:
            pass
    return None, None

def _save_debug_page(html):
    with open(DEBUG_HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

def get_product_info(url, profile_path='./chrome_profile', headless=False):
    playwright = None
    context = None
    try:
        playwright, context = _create_browser_context(profile_path, headless)
        page = context.new_page()
        page.goto(url, wait_until='networkidle', timeout=WAIT_TIMEOUT)
        page.wait_for_timeout(3000)
        _emulate_human_behavior(page)

        html = page.content()
        price, name = _extract_price_from_page(html)

        if price is None:
            _save_debug_page(html)

        result = {
            "store": "DNS",
            "name": name,
            "price_str": f"{price:,.0f} ₽".replace(',', ' '),
            "price_float": price,
            "url": url,
            "extra": {}
        }
        return result

    finally:
        if context:
            context.close()
        if playwright:
            playwright.stop()