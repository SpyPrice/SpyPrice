import sys
from urllib.parse import urlparse

from get_price.get_price_DNS import get_product_info as get_dns_info
from get_price.get_price_Steam import get_game_info as get_steam_info
from get_price.get_price_LisSkins import get_product_info as get_lisskins_info
from get_price.get_price_Sportmaster import get_product_info as get_sportmaster_info
from get_price.get_price_ChitaiGorod import get_product_info as get_chitai_gorod_info
from get_price.get_price_Mosigra import get_product_info as get_mosigra_info
from get_price.get_price_Hobbygames import get_product_info as get_hobbygames_info
from get_price.get_price_Playerok import get_product_info as get_playerok_info
from get_price.get_price_AutoRu import get_product_info as get_auto_ru_info
from get_price.get_price_Avito import get_product_info as get_avito_info


def detect_store(url):
    domain = urlparse(url).netloc.lower()
    if "dns-shop.ru" in domain:
        return "dns"
    elif "steampowered.com" in domain or url.strip().isdigit():
        return "steam"
    elif "lis-skins.com" in domain or "lis-skins.ru" in domain:
        return "lisskins"
    elif "sportmaster.ru" in domain:
        return "sportmaster"
    elif "chitai-gorod.ru" in domain:
        return "chitai_gorod"
    elif "mosigra.ru" in domain:
        return "mosigra"
    elif "hobbygames.ru" in domain:
        return "hobbygames"
    elif "playerok.com" in domain:
        return "playerok"
    elif "auto.ru" in domain:
        return "auto_ru"
    elif "avito.ru" in domain:
        return "avito"
    else:
        return None


def fetch_info(user_input):
    store = detect_store(user_input)

    if store == "steam":
        return get_steam_info(user_input)
    elif store == "dns":
        return get_dns_info(user_input, headless=False)
    elif store == "lisskins":
        return get_lisskins_info(user_input, headless=True)
    elif store == "sportmaster":
        return get_sportmaster_info(user_input, headless=True)
    elif store == "chitai_gorod":
        return get_chitai_gorod_info(user_input, headless=True)
    elif store == "mosigra":
        return get_mosigra_info(user_input, headless=True)
    elif store == "hobbygames":
        return get_hobbygames_info(user_input, headless=True)
    elif store == "playerok":
        return get_playerok_info(user_input, headless=True)
    elif store == "auto_ru":
        return get_auto_ru_info(user_input, headless=True)
    elif store == "avito":
        return get_avito_info(user_input, headless=False)
    else:
        raise ValueError(f"Неподдерживаемый магазин или некорректная ссылка {user_input}")


def print_info(info):
    if not info:
        print("Информация не найдена")
        return

    print(f"\n {info['store']}")
    print(f"Название: {info['name']}")
    print(f"Цена: {info['price_str']}")
    print(f"Ссылка: {info['url']}")

    # Дополнительная информация (не всегда робит)
    extra = info.get('extra', {})
    if info['store'] == 'Steam':
        if extra.get('developers'):
            print(f"Разработчик: {', '.join(extra['developers'])}")
        if extra.get('release_date'):
            print(f"Дата выхода: {extra['release_date']}")
        if extra.get('discount_percent', 0) > 0:
            print(f"Скидка: {extra['discount_percent']}%")
    elif info['store'] == 'LisSkins':
        if extra.get('prices_by_wear'):
            print("Цены по износам:")
            for wear, price in extra['prices_by_wear'].items():
                print(f"  {wear}: ${price:.2f}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = input("Введите ссылку на товар: ").strip()

    try:
        info = fetch_info(user_input)
        print_info(info)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)