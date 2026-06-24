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

        if os.path.exists(profile_dir):
            print(f"Ozon профиль: {profile_dir}")
            prefs_file = os.path.join(profile_dir, 'Default', 'Preferences')
            if os.path.exists(prefs_file):
                print(f"Файл сессии существует: {prefs_file}")
        else:
            print(f"Ozon профиль не найден(({profile_dir}")

        os.makedirs(profile_dir, exist_ok=True)
        self.playwright = await async_playwright().start()
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled'],
            viewport=config.VIEWPORT
        )

    async def _extract_info(self, page, url):
        await page.wait_for_selector('h1', timeout=config.WAIT_TIMEOUT)
        name = (await page.locator("h1").first.text_content()).strip()

        price_selectors = [
            'span.tsHeadline600Large',
            'span[class*="tsHeadline"][class*="Large"]',
            '.c35_3_16-a1.tsHeadline500Medium'
        ]
        price_elem = None
        for selector in price_selectors:
            if await page.locator(selector).first.count() > 0:
                price_elem = page.locator(selector).first
                break
        if not price_elem:
            return None

        price_raw = await price_elem.inner_text()
        price_clean = Decimal(re.sub(r'[^\d]', '', price_raw))
        return {
            'name': name,
            'price_str': f"{price_clean:,} ₽".replace(',', ' '),
            'price': price_clean,
            'extra': {}
        }