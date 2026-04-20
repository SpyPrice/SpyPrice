import asyncio
import re
import os
from decimal import Decimal

from playwright.async_api import async_playwright
from etl.app.base_parser import BaseStoreParser
from etl.app import config


class Ymarket(BaseStoreParser):
    store_name = "yandex market"

    async def _create_browser_context(self):
        profile_dir = os.path.join(config.DEBUG_DIR, 'ymarket-profile')
        os.makedirs(profile_dir, exist_ok=True)
        self.playwright = await async_playwright().start()
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled'],
            viewport=config.VIEWPORT
        )

    async def _extract_info(self, page, url):
        await page.wait_for_selector('[data-auto="productCardTitle"]', timeout=config.WAIT_TIMEOUT)
        await page.wait_for_selector('[data-auto="snippet-price-old"]', timeout=config.WAIT_TIMEOUT)

        await page.wait_for_function(
            """(selector) => {
                const el = document.querySelector(selector);
                return el && el.innerText.trim().match(/\\d/);
            }""",
            arg='[data-auto="snippet-price-old"]',
            timeout=config.WAIT_TIMEOUT
        )

        name = (await page.locator('[data-auto="productCardTitle"]').first.text_content()).strip()

        price_selector = '[data-auto="snippet-price-current"]'
        if not await page.locator(price_selector).first.is_visible():
            price_selector = '[data-auto="snippet-price-old"]'

        price_elem = page.locator('[data-auto="snippet-price-current"], [data-zone-name="price"] .ds-valueLine').first
        price_raw = await price_elem.inner_text()
        price_clean = int(re.sub(r"[^\d]", "", price_raw))

        return {
            'name': name,
            'price_str': f"{price_clean:,} ₽".replace(',', ' '),
            'price': Decimal(price_clean),
            'extra': {}
        }
