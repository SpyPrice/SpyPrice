from app.repository import cards as cards_repository

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker

from app.dependency import get_async_session

import asyncio
from os import getenv
from httpx import AsyncClient
from app.schemas import AskExistsItemParse

from collections import defaultdict
from itertools import zip_longest


# Время в секундах. Пока общее, потом - для каждого магазина своё
frequency_parse = 6 * 60 * 60
item_in_group_count = 10
item_in_group_delta = 45
between_groups_delta = 5 * 60
error_delta = 10 * 60





async def loop(db: AsyncSession):

    while True:
        cards = await cards_repository.get_all_cards_id_source_url(db)

        groups = defaultdict(list)

        # card: id, url, source_id
        print(cards)
        for card in cards:
            groups[card.source_id].append(card)

        print(groups)

        group_count = 0
        for not_same_sources_cards in zip_longest(*groups.values()):
            group_count += 1
            # парсить группу
            for card in not_same_sources_cards:
                if card is not None:
                    await notify_etl_to_parse_exists_item(card.id, card.url, card.source_id)
            await asyncio.sleep(item_in_group_delta)
            if group_count == item_in_group_count:
                group_count = 0
                await asyncio.sleep(between_groups_delta)

        await asyncio.sleep(frequency_parse)


async def notify_etl_to_parse_exists_item(item_id: int, url: str, source_id: int):
    etl_base_url = getenv('ETL_URL', 'http://127.0.0.1:8080')
    backend_base_url = getenv('API_BASE_URL', 'http://127.0.0.1:8000')

    etl_url = f"{etl_base_url}/ask_parse_exists_item"
    callback_url = f"{backend_base_url}/webhook/etl_exists_item_parse_result"

    print(f'Отправляем в etl exists_item {url=}')
    async with AsyncClient() as client:
        try:
            result = await client.post(etl_url, json=AskExistsItemParse(
                item_id=item_id,
                url=url,
                source_id=source_id,
                callback_url=callback_url
            ).model_dump())
            result.raise_for_status()
        except Exception as e:
            print('\n'*3 + f'ошибка связи с ETL: {e}' + '\n'*3)



async def start_loop():
    async with async_session_maker() as session:
        await loop(session)


if __name__ == '__main__':
    asyncio.run(start_loop())

