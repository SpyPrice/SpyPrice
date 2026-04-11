# app/parsers/steam_market.py
import asyncio
import requests
from urllib.parse import quote
from etl.app import config


class SteamMarketParser:
    store_name = "Steam Market"

    def __init__(self, headless=True):
        pass

    async def get_product_info(self, url_or_name):
        """Асинхронная обёртка."""
        return await asyncio.to_thread(self._get_product_info_sync, url_or_name)

    def _get_product_info_sync(self, user_input):
        app_id, market_hash_name = self._extract_params(user_input)
        if not app_id or not market_hash_name:
            raise ValueError("Не удалось определить app_id или market_hash_name")

        # 1. Основная информация о цене
        price_data = self._fetch_price_overview(app_id, market_hash_name)

        # 2. Детальная информация о книге ордеров (опционально)
        histogram_data = self._fetch_orders_histogram(app_id, market_hash_name)

        # Собираем результат
        name = market_hash_name
        price_str = price_data.get('lowest_price', 'Цена не найдена') if price_data else 'Цена не найдена'
        price_float = self._extract_price_float(price_str)
        currency = price_data.get('currency') if price_data else None

        return {
            "store": self.store_name,
            "name": name,
            "price_str": price_str,
            "price_float": price_float,
            "url": f"https://steamcommunity.com/market/listings/{app_id}/{quote(market_hash_name)}",
            "extra": {
                "app_id": app_id,
                "market_hash_name": market_hash_name,
                "currency": currency,
                "volume": price_data.get('volume'),
                "median_price": price_data.get('median_price'),
                "highest_buy_order": histogram_data.get('highest_buy_order') if histogram_data else None,
                "lowest_sell_order": histogram_data.get('lowest_sell_order') if histogram_data else None,
            }
        }

    def _extract_params(self, user_input):
        """Извлекает app_id и market_hash_name из URL или строки."""
        # Пример URL: https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Redline%20(Field-Tested)
        if "steamcommunity.com/market/listings" in user_input:
            parts = user_input.split('/listings/')[1].split('/')
            app_id = parts[0]
            from urllib.parse import unquote
            market_hash_name = unquote(parts[1])
            return app_id, market_hash_name
        # Если это просто название предмета, то нужно знать app_id (например, CS:GO - 730)
        # Для упрощения можно считать, что это CS:GO
        elif user_input and not user_input.startswith("http"):
            return '730', user_input
        return None, None

    def _fetch_price_overview(self, app_id, market_hash_name):
        """Запрашивает данные о цене."""
        try:
            resp = requests.get(
                "https://steamcommunity.com/market/priceoverview/",
                params={
                    'appid': app_id,
                    'currency': '5',  # 5 = RUB, можно вынести в config
                    'market_hash_name': market_hash_name
                },
                timeout=config.STEAM_TIMEOUT
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Ошибка при запросе priceoverview: {e}")
            return None

    def _fetch_orders_histogram(self, app_id, market_hash_name):
        """Запрашивает детальную книгу ордеров."""
        try:
            # Для этого эндпоинта нужно получить item_nameid (можно из HTML страницы листинга)
            # В упрощенном виде можно пропустить или реализовать отдельно
            return None
        except Exception as e:
            print(f"Ошибка при запросе itemordershistogram: {e}")
            return None

    def _extract_price_float(self, price_str):
        """Извлекает число из строки цены."""
        import re
        if not price_str or price_str == 'Цена не найдена':
            return None
        # Удаляем все нецифровые символы, кроме точки и запятой
        cleaned = re.sub(r'[^\d.,]', '', price_str).replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            return None