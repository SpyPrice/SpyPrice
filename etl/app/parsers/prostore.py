import asyncio
import re
import os
import sys
from decimal import Decimal
from typing import Optional, Dict, Any

from etl.app import config
from etl.app.base_parser import BaseStoreParser
from playwright.async_api import Page, async_playwright


class ProstoreParser(BaseStoreParser):
    store_name = "PROSTORE"

    SELECTOR_NAME = '[class*="h-28-400-j"]'
    SELECTOR_PRICE = '.h-36-600-i.price-nowrap'
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

    async def _extract_info(self, page: Page, url: str) -> Optional[Dict[str, Any]]:
        await page.wait_for_selector(self.SELECTOR_NAME, timeout=config.WAIT_TIMEOUT)

        await page.wait_for_selector(self.SELECTOR_NAME, timeout=config.WAIT_TIMEOUT)

        name_locator = page.locator(self.SELECTOR_NAME).first
        if await name_locator.count() > 0:
            name = (await name_locator.inner_text()).strip()

        price_locator = page.locator(self.SELECTOR_PRICE).first
        if await price_locator.count() > 0:
            price_text = await price_locator.inner_text()
            price = self._parse_price(price_text)
        if name and price is not None and price > 0:
            return {
                'name': name,
                'price': price,
                'price_str': f"{price}".replace(',', ' '),
                'currency': 'RUB',
            }
        return None

    def _parse_price(self, price_text: str) -> Optional[Decimal]:
        price = price_text[:-2].replace(' ', '')
        try:
            price = Decimal(price)
            return price
        except:
            return None
