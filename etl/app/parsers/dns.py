import re
import os
from decimal import Decimal

from playwright.async_api import async_playwright
from etl.app.base_parser import BaseStoreParser
from etl.app import config


class DNSParser(BaseStoreParser):
    store_name = "DNS"

    async def _create_browser_context(self):
        profile_dir = os.path.join(config.DEBUG_DIR, 'dns-profile')
        os.makedirs(profile_dir, exist_ok=True)
        self.playwright = await async_playwright().start()
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled'],
            viewport=config.VIEWPORT
        )

    async def _extract_info(self, page, url):
        await page.wait_for_selector('h1.product-card-top__title', timeout=config.WAIT_TIMEOUT)
        name = (await page.locator("h1.product-card-top__title").first.text_content()).strip()

        price_selector = '.product-buy__price_active'
        try:
            await page.wait_for_selector(price_selector, timeout=5000)
        except:
            price_selector = '.product-buy__price'
            await page.wait_for_selector(price_selector, timeout=config.WAIT_TIMEOUT)

        price_elem = page.locator(price_selector).first
        full_text = (await price_elem.inner_text()).strip()

        prev_span = price_elem.locator('.product-buy__prev').first
        if await prev_span.count() > 0:
            prev_text = (await prev_span.inner_text()).strip()
            # Удаляем текст старой цены из общего текста
            full_text = full_text.replace(prev_text, '').strip()

        price_clean = re.sub(r'[^\d]', '', full_text)
        if not price_clean:
            return None

        price = Decimal(price_clean)   # или int(price_clean)
        return {
            'name': name,
            'price_str': f"{price:,.0f} ₽".replace(',', ' '),
            'price': price,
            'currency': 'RUB',
            'extra': {}
        }