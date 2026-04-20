import asyncio
import re
import os
from decimal import Decimal

from playwright.async_api import async_playwright
from etl.app.base_parser import BaseStoreParser
from etl.app import config


class OzonParser(BaseStoreParser):
    store_name = "Ozon"

    async def _create_browser_context(self):
        profile_dir = os.path.join(config.DEBUG_DIR, 'ozon_profile')
        os.makedirs(profile_dir, exist_ok=True)
        self.playwright = await async_playwright().start()
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled'],
            viewport=config.VIEWPORT
        )


    async def _extract_info(self, page, url):
        await page.wait_for_selector('[data-widget="webPrice"], .c2h5, [class*="price"]', timeout=config.WAIT_TIMEOUT)

        name = (await page.locator("h1").first.text_content()).strip()
        await page.wait_for_function(
            """(selector) => {
                const el = document.querySelector(selector);
                return el && el.innerText.trim().match(/\\d/);
            }""",
            arg='span.pdp_bj.tsHeadline500Medium',
            timeout=config.WAIT_TIMEOUT
        )
        price_elem = page.locator('span.pdp_bj.tsHeadline500Medium').first
        price_raw = await price_elem.inner_text(timeout=config.WAIT_TIMEOUT)
        price_clean = int(re.sub(r"[^\d]", "", price_raw))
        return {
            'name': name,
            'price_str': f"{price_clean:,} ₽".replace(',', ' '),
            'price': Decimal(price_clean),
            'extra': {}
        }
