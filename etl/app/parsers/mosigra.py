import re
from ..base_parser import BaseStoreParser
from .. import config


class MosigraParser(BaseStoreParser):
    store_name = "Мосигра"

    async def _extract_info(self, page, url):
        await page.wait_for_timeout(config.WAIT_TIMEOUT)

        ld = await self._extract_json_ld(page)
        if ld:
            return ld

        name_elem = page.locator('h1').first
        name = (await name_elem.text_content()).strip() if await name_elem.count() > 0 else "Неизвестный товар"

        selectors = [
            '.product-buy__price',
            '.product-price',
            '[class*="price"]',
            '.price',
            '.current-price'
        ]
        price_text = None
        for sel in selectors:
            elem = page.locator(sel).first
            if await elem.count() > 0:
                price_text = (await elem.text_content()).strip()
                break

        if not price_text:
            return None

        price_clean = re.sub(r'[^\d.]', '', price_text)
        if not price_clean:
            return None

        return {
            'name': name,
            'price_str': price_text,
            'price_float': float(price_clean),
            'extra': {}
        }