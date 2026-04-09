import json
import re
from playwright.sync_api import sync_playwright

WAIT_TIMEOUT = 30000
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


def _create_browser_context(headless=True):
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless, args=['--disable-blink-features=AutomationControlled'])
    context = browser.new_context(user_agent=USER_AGENT, viewport={'width': 1920, 'height': 1080})
    return playwright, browser, context


def get_product_info(url, headless=True):
    playwright = browser = context = None
    try:
        print(f"Запуск Мосигры")
        playwright, browser, context = _create_browser_context(headless)
        page = context.new_page()
        page.goto(url, wait_until='domcontentloaded', timeout=WAIT_TIMEOUT)
        page.wait_for_timeout(3000)

        html_content = page.content()

        try:
            json_ld_script = page.locator('script[type="application/ld+json"]').first
            if json_ld_script.count() > 0:
                data = json.loads(json_ld_script.inner_text())
                if isinstance(data, list):
                    for item in data:
                        if item.get('@type') == 'Product':
                            data = item
                            break
                name = data.get('name')
                offers = data.get('offers', {})
                price = offers.get('price')
                currency = offers.get('priceCurrency', 'RUB')
                if name and price:
                    price_float = float(price)
                    price_str = f"{price_float:,.2f} {currency}".replace(',', ' ')
                    return {"store": "Мосигра", "name": name, "price_str": price_str, "price_float": price_float,
                            "url": url, "extra": {}}
        except Exception as e:
            print(f"Ошибка {e}")

        name_elem = page.locator('h1').first
        name = name_elem.text_content().strip() if name_elem.count() > 0 else "Неизвестный товар"

        price_selectors = [
            '.product-buy__price',
            '.product-price',
            '[class*="price"]',
            '.price',
            '.current-price'
        ]
        price_text = None
        for selector in price_selectors:
            price_elem = page.locator(selector).first
            if price_elem.count() > 0:
                price_text = price_elem.text_content().strip()
                break

        if price_text:
            price_clean = re.sub(r'[^\d.]', '', price_text)
            if price_clean:
                return {"store": "Мосигра", "name": name, "price_str": price_text, "price_float": float(price_clean),
                        "url": url, "extra": {}}

        with open('mosigra_debug.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        return None

    except Exception as e:
        print(f"Ошибка {e}")
        return None

    finally:
        if context: context.close()
        if browser: browser.close()
        if playwright: playwright.stop()