import asyncio
import re
import os
from decimal import Decimal

from playwright.async_api import async_playwright
from etl.app.base_parser import BaseStoreParser
from etl.app import config


class AutoRuParser(BaseStoreParser):
    store_name = "Авто.ру"

    async def _create_browser_context(self):
        profile_dir = os.path.join(config.DEBUG_DIR, 'avtoru-profile')
        os.makedirs(profile_dir, exist_ok=True)
        self.playwright = await async_playwright().start()
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled'],
            viewport=config.VIEWPORT
        )

    async def _extract_info(self, page, url):
        await page.wait_for_selector('h1.CardHead__title', timeout=config.WAIT_TIMEOUT)
        await page.wait_for_selector('.PriceUsedOfferNew__price-VRrW8 .OfferPriceCaption__price', timeout=config.WAIT_TIMEOUT)

        name = (await page.locator('h1.CardHead__title').first.text_content()).strip()
        print(name)
        await page.wait_for_function(
            """(selector) => {
                const el = document.querySelector(selector);
                return el && el.innerText.trim().match(/\\d/);
            }""",
            arg='.PriceUsedOfferNew__price-VRrW8 .OfferPriceCaption__price',
            timeout=config.WAIT_TIMEOUT
        )

        name = (await page.locator('h1.CardHead__title').first.text_content()).strip()

        price_elem = page.locator('.PriceUsedOfferNew__price-VRrW8 .OfferPriceCaption__price').first
        price_raw = await price_elem.inner_text()
        price_clean = int(re.sub(r"[^\d]", "", price_raw))

        return {
            'name': name,
            'price_str': f"{price_clean:,} ₽".replace(',', ' '),
            'price': Decimal(price_clean),
            'extra': {}
        }