import re
from ..base_parser import BaseStoreParser
from .. import config


class AutoRuParser(BaseStoreParser):
    store_name = "Авто.ру"

    async def _extract_info(self, page, url):
        await page.wait_for_timeout(config.WAIT_TIMEOUT)

        try:
            script = page.locator('script[type="application/ld+json"]').first
            if await script.count() > 0:
                import json
                text = await script.inner_text()
                data = json.loads(text)
                if '@graph' in data:
                    for item in data['@graph']:
                        if item.get('@type') in ('Product', 'Car'):
                            data = item
                            break
                name = data.get('name')
                offers = data.get('offers', {})
                price = offers.get('price')
                currency = offers.get('priceCurrency', 'RUB')
                if name and price is not None:
                    return {
                        'name': name,
                        'price_float': float(price),
                        'price_str': f"{float(price):,.2f} {currency}".replace(',', ' '),
                        'extra': {}
                    }
        except Exception:
            pass

        name_elem = page.locator('h1').first
        name = (await name_elem.text_content()).strip() if await name_elem.count() > 0 else "Неизвестный автомобиль"

        selectors = ['.CardInfo__price', '[class*="price"]', '.Price__value']
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