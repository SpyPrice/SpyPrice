import re
from ..base_parser import BaseStoreParser
from .. import config


class HobbygamesParser(BaseStoreParser):
    store_name = "Хоббигеймс"

    async def _extract_info(self, page, url):
        await page.wait_for_timeout(config.WAIT_TIMEOUT)

        ld = await self._extract_json_ld(page)
        if ld:
            return ld

        name_elem = page.locator('h1').first
        name = (await name_elem.text_content()).strip() if await name_elem.count() > 0 else "Неизвестный товар"

        price_elem = page.locator('[class*="price"], .product-price, .current-price').first
        if await price_elem.count() == 0:
            return None

        price_text = (await price_elem.text_content()).strip()
        price_clean = re.sub(r'[^\d.]', '', price_text)
        if not price_clean:
            return None

        return {
            'name': name,
            'price_str': price_text,
            'price_float': float(price_clean),
            'extra': {}
        }