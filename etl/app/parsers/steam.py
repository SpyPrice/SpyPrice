import asyncio
from decimal import Decimal

import requests
from .. import config
from typing import Optional, Dict, Any
import logging

class SteamParser:
    store_name = "Steam"

    def __init__(self, headless=True):
        pass

    async def get_product_info(self, url_or_id: str) -> Optional[Dict[str, Any]]:
        return await asyncio.to_thread(self._get_product_info_sync, url_or_id)

    def _get_product_info_sync(self, url_or_id: str) -> Optional[Dict[str, Any]]:
        if "store.steampowered.com/app/" in url_or_id:
            try:
                app_id = url_or_id.split('/app/')[1].split('/')[0]
            except IndexError:
                app_id = url_or_id.strip()
        else:
            app_id = url_or_id.strip()

        if not app_id.isdigit():
            raise ValueError("Неверный идентификатор приложения Steam")

        try:
            resp = requests.get(
                config.STEAM_API_URL,
                params={'appids': app_id, 'cc': 'ru', 'l': 'russian'},
                timeout=config.STEAM_TIMEOUT
            )
            resp.raise_for_status()
            data = resp.json()
            if not data[str(app_id)]["success"]:
                return None
            game = data[str(app_id)]["data"]

            name = game.get("name")
            is_free = game.get("is_free", False)
            price_info = game.get("price_overview", {})

            if is_free:
                price_str = "Бесплатно"
                price = 0
            elif price_info:
                price_str = price_info.get("final_formatted", "Цена не указана")
                price = Decimal(price_info.get("final", 0)) / 100
            else:
                price_str = "Цена не найдена"
                price = None

            if price is None:
                return None

            return {
                "store": self.store_name,
                "name": name,
                "price_str": price_str,
                "price": Decimal(price),
                "url": f"https://store.steampowered.com/app/{app_id}",
                "currency": price_info.get("currency", "RUB")
            }
        except Exception as e:
            logging.error(f"Ошибка Steam API: {e}")
            return None