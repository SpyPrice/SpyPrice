from urllib.parse import urlparse

from .steam import SteamParser
from .dns import DNSParser
#from .ozon import OzonParser
#from .sportmaster import SportmasterParser
from .lisskins import LisSkinsParser
from .mosigra import MosigraParser
from .hobbygames import HobbygamesParser
from .chitai_gorod import ChitaiGorodParser
from .playerok import PlayerokParser
#from .auto_ru import AutoRuParser
#from .avito import AvitoParser
from .steam_market import SteamMarketParser


def detect_store(url):
    domain = urlparse(url).netloc.lower()
    full_url = url.lower()

    match domain:
        case d if "dns-shop.ru" in d:
            return "dns"
        case d if "steampowered.com" in d:
            return "steam"
        case d if "steamcommunity.com" in d:
            return "steam_market"
        case d if "ozon.ru" in d:
            return "ozon"
        case d if "lis-skins.com" in d:
            return "lisskins"
        case d if "sportmaster.ru" in d:
            return "sportmaster"
        case d if "chitai-gorod.ru" in d:
            return "chitai_gorod"
        case d if "mosigra.ru" in d:
            return "mosigra"
        case d if "hobbygames.ru" in d:
            return "hobbygames"
        case d if "playerok.com" in d:
            return "playerok"
        case d if "auto.ru" in d:
            return "auto_ru"
        case d if "avito.ru" in d:
            return "avito"
        case _:
            return None


def get_parser(store_key, headless=True):
    match store_key:
        case "steam":
            return SteamParser(headless)
        case "steam_market":
            return SteamMarketParser(headless)
        case "dns":
            return DNSParser(headless)
        #case "ozon":
        #    return OzonParser(headless)
        case "lisskins":
            return LisSkinsParser(headless)
        #case "sportmaster":
        #    return SportmasterParser(headless)
        case "chitai_gorod":
            return ChitaiGorodParser(headless)
        case "mosigra":
            return MosigraParser(headless)
        case "hobbygames":
            return HobbygamesParser(headless)
        case "playerok":
            return PlayerokParser(headless)
        #case "auto_ru":
        #    return AutoRuParser(headless)
        #case "avito":
        #    return AvitoParser(headless)
        case _:
            raise ValueError(f"Неподдерживаемый магазин: {store_key}")