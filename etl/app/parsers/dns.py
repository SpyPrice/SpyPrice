import re
from ..base_parser import BaseStoreParser
from .. import config


class DNSParser(BaseStoreParser):
    store_name = "DNS"

    async def _extract_info(self, page, url):
        await page.wait_for_selector('h1', timeout=config.WAIT_TIMEOUT)

        ld = await self._extract_json_ld(page)
        if ld:
            return ld

        name_elem = page.locator('h1').first
        name = (await name_elem.text_content()).strip() if await name_elem.count() > 0 else "Неизвестный товар"

        price_elem = page.locator('.product-buy__price').first
        if await price_elem.count() == 0:
            return None

        price_text = (await price_elem.text_content()).strip()
        price_clean = re.sub(r'[^\d.]', '', price_text.replace('\xa0', '').replace(' ', ''))
        if not price_clean:
            return None

        price_float = float(price_clean)
        return {
            'name': name,
            'price_str': f"{price_float:,.0f} ₽".replace(',', ' '),
            'price_float': price_float,
            'extra': {}
        }