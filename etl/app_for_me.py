import sys
import asyncio
from typing import Optional

from app.choose_parser import get_parser, detect_store


async def async_main(user_input):
    store_key = detect_store(user_input)
    if not store_key:
        print("Не удалось определить магазин")
        return

    parser = get_parser(store_key, headless=True)
    info = await parser.get_product_info(user_input)
    print_info(info)

def print_info(info):
    if not info:
        print("Информация не найдена")
        return

    #print(f"{info['store']}")
    print(f"Название: {info['name']}")
    print(f"Цена: {info['price']}")
    print(f"Ссылка: {info['url']}")

if __name__ == '__main__':
    while True:
        user_input = input("Введите ссылку на товар: ").strip()
        try:
            asyncio.run(async_main(user_input))
        except Exception as e:
            print(f"Ошибка: {e}")