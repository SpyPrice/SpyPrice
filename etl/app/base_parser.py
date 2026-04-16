import json
import re
import os
import asyncio
import random
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Optional, Dict
import logging

from playwright.async_api import async_playwright, Page
from . import config


class BaseStoreParser(ABC):
    store_name = "BaseStore"

    def __init__(self, headless=True):
        self.headless = headless
        self.debug_subdir = os.path.join(config.DEBUG_DIR, self.store_name.lower().replace(' ', '_'))
        os.makedirs(self.debug_subdir, exist_ok=True)

    async def _create_browser_context(self) -> None:
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = await self.browser.new_context(
            user_agent=config.USER_AGENT,
            viewport=config.VIEWPORT
        )

    async def _close_browser(self) -> None:
        if hasattr(self, 'context') and self.context:
            await self.context.close()
        if hasattr(self, 'browser') and self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright') and self.playwright:
            await self.playwright.stop()

    async def _emulate_human(self, page) -> None:
        await page.mouse.move(random.randint(100, 500), random.randint(100, 500))
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.3);")
        await page.wait_for_timeout(1500)

    async def _save_debug(self, page, prefix='error') -> None:
        timestamp = int(await page.evaluate("() => Date.now()"))
        screenshot_path = os.path.join(self.debug_subdir, f'{prefix}_{timestamp}.png')
        html_path = os.path.join(self.debug_subdir, f'{prefix}_{timestamp}.html')
        await page.screenshot(path=screenshot_path)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(await page.content())
        logging.DEBUG(f"Отладочные файлы сохранены: {screenshot_path}, {html_path}")

    async def _extract_json_ld(self, page: Page) -> Optional[Dict[str, Any]]:
        try:
            script = page.locator('script[type="application/ld+json"]').first
            if await script.count() == 0:
                return None
            text = await script.inner_text()
            data = json.loads(text)
            if isinstance(data, list):
                for item in data:
                    if item.get('@type') == 'Product':
                        data = item
                        break
            if data.get('@type') == 'Product':
                name = data.get('name')
                offers = data.get('offers', {})
                if isinstance(offers, list) and offers:
                    offers = offers[0]

                if isinstance(offers, dict):
                    if offers.get('@type') == 'AggregateOffer':
                        price = offers.get('lowPrice')
                        currency = offers.get('priceCurrency', 'RUB')
                    else:
                        price = offers.get('price')
                        currency = offers.get('priceCurrency', 'RUB')
                    if name and price is not None:
                        return {
                            'name': name,
                            'price': Decimal(price),
                            'price_str': f"{price:,.2f} {currency}".replace(',', ' '),
                            'currency': currency
                        }
        except Exception:
            pass
        return None

    @abstractmethod
    async def _extract_info(self, page: Page, url: str) -> Optional[Dict[str, Any]]:
        pass

    async def get_product_info(self, url: str) -> Optional[Dict[str, Any]]:
        page = None
        try:
            await self._create_browser_context()
            page = await self.context.new_page()
            await page.goto(url, wait_until='domcontentloaded', timeout=config.PAGE_LOAD_TIMEOUT)
            await self._emulate_human(page)

            content = await page.content()
            if await page.locator('#challenge-form').count() > 0 or 'Checking your browser' in content:
                await self._save_debug(page, 'captcha')
                return None

            info = await self._extract_info(page, url)
            if not info:
                await self._save_debug(page, 'no_info')
                return None

            return {
                "store": self.store_name,
                "name": info['name'],
                "price_str": info['price_str'],
                "price": info['price'],
                "url": url,
            }
        except Exception as e:
            logging.error(e)
            if page:
                await self._save_debug(page, 'exception')
            return None
        finally:
            await self._close_browser()