import asyncio
import re
import os
import sys
from decimal import Decimal
from typing import Optional, Dict, Any

from etl.app import config
from etl.app.base_parser import BaseStoreParser
from playwright.async_api import Page


class GGselParser(BaseStoreParser):
    store_name = "GGsel"

    SELECTOR_NAME = 'h1[class*="Product"][class$="__title"]'
    SELECTOR_PRICE = '[data-testid="product-price"]'

    async def _extract_info(self, page: Page, url: str) -> Optional[Dict[str, Any]]:
        name = None
        price = None
        currency = 'RUB'

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
                'price_str': f"{price:,.2f} {currency}".replace(',', ' '),
                'currency': 'RUB',
            }
        return None

    def _parse_price(self, price_text: str) -> Optional[Decimal]:
        try:
            price_text = re.sub(r'\s+', '', price_text)
            price = re.search(r'[\d.,]+', price_text).group(0).replace(',', '.')
            price = Decimal(price)
            return price
        except:
            return None
