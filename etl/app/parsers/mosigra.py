import re
from decimal import Decimal

from ..base_parser import BaseStoreParser
from .. import config
from playwright.async_api import Page
from typing import Dict, Any, Optional

class MosigraParser(BaseStoreParser):
    store_name = "Мосигра"

    async def _extract_info(self, page: Page, url: str) -> Optional[Dict[str, Any]]:
        await page.wait_for_selector('.product__header-inner h1', timeout=config.WAIT_TIMEOUT)
        await page.wait_for_selector(".buy-wrapper__big-text .h1", state="attached", timeout=config.WAIT_TIMEOUT)

        name_elem = page.locator('.product__header-inner h1').first
        name = (await name_elem.text_content()).strip() if await name_elem.count() > 0 else "Неизвестный товар"


        price_elem = page.locator(".buy-wrapper__big-text .h1").first
        if await price_elem.count() == 0:
            return None

        price_text = (await price_elem.text_content()).strip()
        price_part = price_text.split()[0] if price_text else ''
        price_clean = re.sub(r'[^\d.]', '', price_part)


        return {
            'name': name,
            'price_str': price_text,
            'price': Decimal(price_clean),
            'currency': 'RUB'
        }