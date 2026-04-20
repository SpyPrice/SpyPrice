import asyncio
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
        await page.wait_for_load_state("networkidle")
        await page.wait_for_selector('h1.product-card-top__title', timeout=config.WAIT_TIMEOUT)
        await page.wait_for_selector('.product-buy__price', timeout=config.WAIT_TIMEOUT)

        name = (await page.locator("h1.product-card-top__title").first.text_content()).strip()
        await page.wait_for_function(
            """(selector) => {
                const el = document.querySelector(selector);
                return el && el.innerText.trim().match(/\\d/);
            }""",
            arg='.product-buy__price',
            timeout=config.WAIT_TIMEOUT
        )
        price_elem = page.locator('.product-buy__price').first
        price_raw = await price_elem.inner_text(timeout=config.WAIT_TIMEOUT)
        price_clean = int(re.sub(r"[^\d]", "", price_raw))
        return {
            'name': name,
            'price_str': f"{price_clean:,} ₽".replace(',', ' '),
            'price': Decimal(price_clean),
            'extra': {}
        }
