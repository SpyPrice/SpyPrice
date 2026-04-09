import json
import re
from playwright.sync_api import sync_playwright

WAIT_TIMEOUT = 30000
DEBUG_HTML_FILE = 'lisskins_debug.html'


def _create_browser_context(headless=True):
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=headless,
        args=['--disable-blink-features=AutomationControlled']
    )
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1920, 'height': 1080}
    )
    return playwright, browser, context


def get_product_info(url, headless=True):
    playwright = browser = context = None
    try:
        print(f"Запуск LisSkins")
        playwright, browser, context = _create_browser_context(headless)
        page = context.new_page()

        page.goto(url, wait_until='domcontentloaded', timeout=WAIT_TIMEOUT)

        page.wait_for_selector('h1', timeout=15000)
        page.wait_for_timeout(2000)

        html = page.content()

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        script_tag = soup.find('script', type='application/ld+json')
        if script_tag:
            try:
                data = json.loads(script_tag.string)
                name = data.get('name')
                offers = data.get('offers', {})
                price = offers.get('lowPrice') or offers.get('price')
                currency = offers.get('priceCurrency', 'RUB')

                if price:
                    price_str = f"{price:,.2f}".replace(',', ' ').replace('.',
                                                                          ',') if currency == 'RUB' else f"${price:,.2f}"

                    result = {
                        "store": "LisSkins",
                        "name": name,
                        "price_str": f"{price_str} {currency}",
                        "price_float": float(price),
                        "url": url,
                        "extra": {
                            "currency": currency,
                            "availability": offers.get('availability')
                        }
                    }
                    return result
            except json.JSONDecodeError:
                pass

        price_elem = page.locator('.skin-min-price .min-price-value').first
        if price_elem.count() > 0:
            price_text = price_elem.text_content().strip()
            price_clean = re.sub(r'[^\d.]', '', price_text)
            price_float = float(price_clean) if price_clean else None

            name_elem = page.locator('h1').first
            name = name_elem.text_content().strip() if name_elem.count() > 0 else "Неизвестно"

            if price_float:
                result = {
                    "store": "LisSkins",
                    "name": name,
                    "price_str": price_text,
                    "price_float": price_float,
                    "url": url,
                    "extra": {}
                }
                return result

        return None

    except Exception as e:
        print(f"Ошибка: {e}")
        if page:
            page.screenshot(path='lisskins_error.png')
        return None
    finally:
        if context:
            context.close()
        if browser:
            browser.close()
        if playwright:
            playwright.stop()