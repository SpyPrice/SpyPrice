import json
import random
import re
from playwright.sync_api import sync_playwright

WAIT_TIMEOUT = 30000
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'


def _create_browser_context(headless=True):
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=headless,
        args=['--disable-blink-features=AutomationControlled']
    )
    context = browser.new_context(
        user_agent=USER_AGENT,
        viewport={'width': 1920, 'height': 1080}
    )
    return playwright, browser, context


def _emulate_human_behavior(page):
    page.mouse.move(random.randint(100, 500), random.randint(100, 500))
    page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.3);")
    page.wait_for_timeout(1500)


def _extract_product_info(page):
    try:
        page.wait_for_selector('h1, .product-price, [class*="price"]', timeout=10000)
    except:
        return None

    try:
        json_ld_script = page.locator('script[type="application/ld+json"]').first
        if json_ld_script.count() > 0:
            data = json.loads(json_ld_script.inner_text())
            name = data.get('name')
            offers = data.get('offers', {})
            price = offers.get('price')
            price_currency = offers.get('priceCurrency', 'RUB')

            if name and price:
                return {
                    "name": name,
                    "price_str": f"{float(price):,.2f} {price_currency}".replace(',', ' '),
                    "price_float": float(price)
                }
    except Exception as e:
        print(f"{e}")

    name_elem = page.locator('h1').first
    name = name_elem.text_content().strip() if name_elem.count() > 0 else "Неизвестный товар"

    price_elem = page.locator('[class*="price"], .product-price, .sale-price, .regular-price').first
    if price_elem.count() > 0:
        price_text = price_elem.text_content().strip()
        price_clean = re.sub(r'[^\d.]', '', price_text)
        if price_clean:
            return {
                "name": name,
                "price_str": price_text,
                "price_float": float(price_clean)
            }

    return None


def get_product_info(url, headless=True):
    playwright = None
    browser = None
    context = None

    try:
        print(f"Запуск браузера для Спортмастер ({'headless' if headless else 'видимый режим'})...")
        playwright, browser, context = _create_browser_context(headless)
        page = context.new_page()

        print(f"Переход на страницу: {url}")
        page.goto(url, wait_until='domcontentloaded', timeout=WAIT_TIMEOUT)

        page.wait_for_timeout(3000)

        _emulate_human_behavior(page)

        if page.locator('#challenge-form').count() > 0 or 'Checking your browser' in page.content():
            page.screenshot(path='sportmaster_challenge.png')
            return None

        product_info = _extract_product_info(page)

        if not product_info:
            page.screenshot(path='sportmaster_error.png')
            with open('sportmaster_debug.html', 'w', encoding='utf-8') as f:
                f.write(page.content())
            return None

        result = {
            "store": "Спортмастер",
            "name": product_info["name"],
            "price_str": product_info["price_str"],
            "price_float": product_info["price_float"],
            "url": url,
            "extra": {}
        }
        return result

    except Exception as e:
        print(f"Ошибка {e}")
        if 'page' in locals():
            page.screenshot(path='sportmaster_error.png')
        return None

    finally:
        if context:
            context.close()
        if browser:
            browser.close()
        if playwright:
            playwright.stop()