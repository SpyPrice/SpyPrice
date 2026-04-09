import json
import requests

STEAM_STORE_API = "https://store.steampowered.com/api/appdetails"
REQUEST_TIMEOUT = 30
DEBUG_FILE = 'steam_debug_response.json'

def extract_app_id(user_input):
    if "store.steampowered.com/app/" in user_input:
        try:
            app_id = user_input.split('/app/')[1].split('/')[0]
            return app_id
        except IndexError:
            pass
    return user_input.strip()

def get_game_info(url_or_id):
    app_id = extract_app_id(url_or_id)
    if not app_id.isdigit():
        raise ValueError("не робит API")

    try:
        params = {
            'appids': app_id,
            'cc': 'ru',
            'l': 'russian'
        }
        response = requests.get(STEAM_STORE_API, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        if not data[str(app_id)]["success"]:
            return None

        game_data = data[str(app_id)]["data"]

        name = game_data.get("name")
        is_free = game_data.get("is_free", False)
        price_info = game_data.get("price_overview", {})

        if is_free:
            price_str = "Бесплатно"
            price_float = 0.0
        elif price_info:
            price_str = price_info.get("final_formatted", "Цена не указана")
            price_float = price_info.get("final", 0) / 100
        else:
            price_str = "Цена не найдена"
            price_float = None

        result = {
            "store": "Steam",
            "name": name,
            "price_str": price_str,
            "price_float": price_float,
            "url": f"https://store.steampowered.com/app/{app_id}",
            "extra": {
                "app_id": app_id,
                "is_free": is_free,
                "currency": price_info.get("currency"),
                "discount_percent": price_info.get("discount_percent", 0),
                "developers": game_data.get("developers", []),
                "publishers": game_data.get("publishers", []),
                "release_date": game_data.get("release_date", {}).get("date")
            }
        }
        return result

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети или запроса {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON {e}")
        with open(DEBUG_FILE, 'w', encoding='utf-8') as f:
            f.write(response.text)
    except Exception as e:
        print(f"Неизвестная ошибка {e}")

    return None