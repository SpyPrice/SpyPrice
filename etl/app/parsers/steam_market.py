import asyncio
import requests
from urllib.parse import quote
from decimal import Decimal
import re
from typing import Optional, Dict, Any
from .. import config
import logging

class SteamMarketParser:
    store_name = "Steam Market"

    def __init__(self, headless=True):
        pass

    async def get_product_info(self, url_or_name: str)  -> Optional[Dict[str, Any]]:
        return await asyncio.to_thread(self._get_product_info_sync, url_or_name)

    def _get_product_info_sync(self, user_input: str) -> Optional[Dict[str, Any]]:
        app_id, market_hash_name = self._extract_params(user_input)
        if not app_id or not market_hash_name:
            raise ValueError("Не удалось определить app_id или market_hash_name")

        price_data = self._fetch_price_overview(app_id, market_hash_name)

        name = market_hash_name
        price_str = price_data.get('lowest_price', 'Цена не найдена') if price_data else 'Цена не найдена'
        price = self._extract_price(price_str)
        currency = price_data.get('currency') if price_data else None

        return {
            "name": name,
            "price_str": price_str,
            "price": price,
            "url": f"https://steamcommunity.com/market/listings/{app_id}/{quote(market_hash_name)}",
            "currency": currency
        }

    def _extract_params(self, user_input):
        if "steamcommunity.com/market/listings" in user_input:
            parts = user_input.split('/listings/')[1].split('/')
            app_id = parts[0]
            from urllib.parse import unquote
            market_hash_name = unquote(parts[1])
            return app_id, market_hash_name
        elif user_input and not user_input.startswith("http"):
            return '730', user_input
        return None, None

    def _fetch_price_overview(self, app_id, market_hash_name):
        try:
            resp = requests.get(
                "https://steamcommunity.com/market/priceoverview/",
                params={
                    'appid': app_id,
                    'currency': '5',
                    'market_hash_name': market_hash_name
                },
                timeout=config.STEAM_TIMEOUT
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logging.error(f"Ошибка при запросе priceoverview: {e}")
            return None

    def _fetch_orders_histogram(self, app_id, market_hash_name):
        try:
            return None
        except Exception as e:
            logging.error(f"{e}")
            return None

    def _extract_price(self, price_str) :
        import re
        if not price_str or price_str == 'Цена не найдена':
            return None
        cleaned = re.sub(r'[^\d.,]', '', price_str).replace(',', '.').rstrip('.')
        try:
            return Decimal(cleaned)
        except ValueError:
            return None