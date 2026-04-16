import re
from decimal import Decimal

from ..base_parser import BaseStoreParser
from .. import config
from playwright.async_api import Page
from typing import Dict, Any, Optional


class LisSkinsParser(BaseStoreParser):
    store_name = "LisSkins"

    async def _extract_info(self, page: Page, url: str) -> Optional[Dict[str, Any]]:
        await page.wait_for_selector('h1', timeout=config.WAIT_TIMEOUT)

        ld = await self._extract_json_ld(page)
        if ld:
            return ld

        price_elem = page.locator('.skin-min-price .min-price-value').first
        if await price_elem.count() == 0:
            return None

        price_text = (await price_elem.text_content()).strip()
        price_part = price_text.split()[0] if price_text else ''
        price_clean = re.sub(r'[^\d.]', '', price_part)
        if not price_clean or price_clean.count('.') > 1:
            return None

        name_elem = page.locator('h1').first
        name = (await name_elem.text_content()).strip() if await name_elem.count() > 0 else "Неизвестно"

        return {
            'name': name,
            'price_str': price_text,
            'price': Decimal(price_clean),
            'currency': 'RUB'
        }