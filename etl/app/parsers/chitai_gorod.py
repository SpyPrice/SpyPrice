import re
from decimal import Decimal
from typing import Optional, Dict, Any
from playwright.async_api import Page

from ..base_parser import BaseStoreParser
from .. import config

class ChitaiGorodParser(BaseStoreParser):
    store_name = "Читай-город"

    async def _extract_info(self, page: Page, url: str) -> Optional[Dict[str, Any]]:
        await page.wait_for_selector('h1', timeout=config.WAIT_TIMEOUT)

        ld = await self._extract_json_ld(page)
        if ld:
            return ld

        name_elem = page.locator('h1').first
        name = (await name_elem.text_content()).strip() if await name_elem.count() > 0 else "Неизвестная книга"

        price_selectors = [
            'meta[itemprop="price"]',
            '.product-offer-price__actual',
        ]

        price_text = None
        for sel in price_selectors:
            elem = page.locator(sel).first
            if await elem.count() > 0:
                if sel.startswith('meta'):
                    price_text = await elem.get_attribute('content')
                else:
                    price_text = (await elem.text_content()).strip()
                if price_text:
                    break

        if not price_text:
            return None

        if '.' in price_text:
            price = Decimal(re.sub(r'[^\d.]', '', price_text))
        else:
            price_clean = re.sub(r'[^\d]', '', price_text)
            if not price_clean:
                return None
            price = Decimal(price_clean)

        price_formatted = f"{price:,} руб".replace(',', ' ')

        return {
            'name': name,
            'price_str': price_formatted,
            'price': price,
            'currency': 'RUB'
        }