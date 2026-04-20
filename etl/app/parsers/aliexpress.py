import asyncio
import re
import os
from decimal import Decimal

from playwright.async_api import async_playwright
from etl.app.base_parser import BaseStoreParser
from etl.app import config


class AliExpress(BaseStoreParser):
    store_name = "Ali Express"

    async def _create_browser_context(self):
        profile_dir = os.path.join(config.DEBUG_DIR, 'aliexpress-profile')
        os.makedirs(profile_dir, exist_ok=True)
        self.playwright = await async_playwright().start()
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled'],
            viewport=config.VIEWPORT
        )

    async def _extract_info(self, page, url):
        await page.wait_for_selector('h1[class*="HazeProductDescription_HazeProductDescription__name"]',
                                     timeout=config.WAIT_TIMEOUT)
        await page.wait_for_selector('div[data-unformatted-price]', timeout=config.WAIT_TIMEOUT)

        name = await page.locator('h1[class*="HazeProductDescription_HazeProductDescription__name"]').first.text_content()
        name = name.strip()

        price_elem = page.locator('div[data-unformatted-price]').first
        price_raw = await price_elem.get_attribute('data-unformatted-price')
        price_clean = int(price_raw)

        return {
            'name': name,
            'price_str': f"{price_clean:,} ₽".replace(',', ' '),
            'price': Decimal(price_clean),
            'extra': {}
        }
