import asyncio
import re
import os
from decimal import Decimal

from playwright.async_api import async_playwright
from etl.app.base_parser import BaseStoreParser
from etl.app import config


class AvitoParser(BaseStoreParser):
    store_name = "Авито"

    async def _create_browser_context(self):
        profile_dir = os.path.join(config.DEBUG_DIR, 'avito-profile')
        os.makedirs(profile_dir, exist_ok=True)
        self.playwright = await async_playwright().start()
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled'],
            viewport=config.VIEWPORT
        )

    async def _extract_info(self, page, url):
        await page.wait_for_selector('h1[data-marker="item-view/title-info"]', timeout=config.WAIT_TIMEOUT)
        name = await page.locator('h1[data-marker="item-view/title-info"]').first.inner_text()

        price_meta = await page.query_selector('meta[itemprop="price"]')
        if not price_meta:
            price_meta = await page.query_selector('meta[property="product:price:amount"]')
        if price_meta:
            price_clean = int(await price_meta.get_attribute('content'))
        else:
            price_locator = page.locator('span[data-marker="item-view/item-price"]').first
            await price_locator.wait_for(state="visible", timeout=config.WAIT_TIMEOUT)
            price_raw = await price_locator.inner_text()
            price_clean = int(re.sub(r"[^\d]", "", price_raw))

        return {
            'name': name,
            'price_str': f"{price_clean:,} ₽".replace(',', ' '),
            'price': Decimal(price_clean),
            'extra': {}
        }
