import sys
import asyncio
from time import sleep
from typing import Optional

from etl.app.choose_parser import get_parser, detect_store

async def async_main(user_input):
    store_key = detect_store(user_input)
    if not store_key:
        print("Не удалось определить магазин")
        return

    parser = get_parser(store_key, headless=True)
    info = await parser.get_product_info(user_input)
    if not info:
        raise Exception()
    else:
            print(f"Название: {info['name']}")
            print(f"Цена: {info['price']}")
            print(f"Ссылка: {info['url']}")

async def test_parser(user_input):
    try:
        await asyncio.wait_for(async_main(user_input), timeout=30000.0)
        await asyncio.sleep(10)  # теперь await корректен
        return True
    except Exception:
        return False


if __name__ == '__main__':
    dict = {"dns" : "https://www.dns-shop.ru/product/adda8fcf8dd3d0a4/63-smartfon-apple-iphone-17-256-gb-cernyj",
            "chitai-gorod" : "https://www.chitai-gorod.ru/product/magicheskaya-bitva-kniga-12-zvezda-i-neft-proklyatyy-plod-vozvrashchenie-3072755",
            "steam" : "https://store.steampowered.com/app/1229490/ULTRAKILL",
            "steamcommunity" : "https://steamcommunity.com/market/listings/730/Dreams%20%26%20Nightmares%20Case",
            "aliexpress" : "https://aliexpress.ru/item/1005008751366847.html",
            "ozon" : "https://www.ozon.ru/product/nastolnye-nastennye-perekidnye-chasy-flip-clock-3834992086",
            "auto.ru" : "https://auto.ru/cars/new/group/tank/700/24011362/24011414/1130383157-6b657180/",
            "avito" : "https://www.avito.ru/moskva/noutbuki/macbook_air_13_m1_8gb_256gb_8086993691",            
            "ggsel" : "https://ggsel.net/catalog/product/antigravity-google-ai-pro-12-mesiacev-gemini-3-0-pro-veo-5tb-liuboi-region-102178065",
            "citilink" : "https://www.citilink.ru/product/noutbuk-chuwi-gamebook-ryzen-9-9955hx-32gb-ssd1tb-rtx5070ti-16-ips-qhd-2090618",
            "hobbygames" : "https://hobbygames.ru/catan-3d-edition",
            "lis-skins" : "https://lis-skins.com/ru/market/csgo/ak-47-gold-arabesque-minimal-wear",
            "mosigra" : "https://www.mosigra.ru/kruti-rolli",
            "mvideo" : "https://www.mvideo.ru/products/smartfon-apple-iphone-17-256gb-blue-bez-rustore-30087003",
            "playerok" : "https://playerok.com/products/c7a687b83150-250k-zolotaclash-royale",
            "prostoe-protechno" : "https://prostore-protechno.ru/shop/macbook-air/apple-macbook-air-13-m4-cpu10c-gpu-2025-16-gb-256-gb-ssd-silver",   
            "yandex.market" : "https://market.yandex.ru/card/umnyy-sudoku-giiker-smart-sudoku-jksd001-s-led-displeyem-dlya-intellektualnykh-igr-universalnyy/4433071424"}
    listi = []
    for (i, j) in dict.items():
        success = False
        for attempt in range(3):
            try:
                result = asyncio.run(test_parser(j.strip()))
                if result:
                    success = True
                    break
            except Exception:
                pass   
        if success:
            print(f"Парсер {i} работает")
            listi.append(i)
    print("Работающие парсеры: "+" ".join(listi))