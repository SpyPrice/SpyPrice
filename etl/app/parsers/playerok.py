import re
from decimal import Decimal

from ..base_parser import BaseStoreParser
from .. import config
from playwright.async_api import Page
from typing import Any, Optional, Dict


class PlayerokParser(BaseStoreParser):
    store_name = "Playerok"

    async def _extract_info(self, page: Page, url: str) -> Optional[Dict[str, Any]]:
        await page.wait_for_selector('h1', timeout=config.WAIT_TIMEOUT)

        ld = await self._extract_json_ld(page)
        if ld:
            return ld

        name_elem = page.locator('h1').first
        name = (await name_elem.text_content()).strip() if await name_elem.count() > 0 else "Неизвестный товар"

        price_elem = page.locator('[class*="price"], .product-price, .item-price').first
        if await price_elem.count() == 0:
            return None

        price_text = (await price_elem.text_content()).strip()
        price_clean = re.sub(r'[^\d.]', '', price_text)
        if not price_clean:
            return None

        return {
            'name': name,
            'price_str': price_text,
            'price': Decimal(price_clean),
            'currency': 'RUB'
        }