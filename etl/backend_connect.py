from httpx import AsyncClient
from fastapi import FastAPI, BackgroundTasks

from etl.app.schemas import AskNewItemParse, ItemCreateWithPriceSnapshot, ParseError
from etl.app.choose_parser import get_parser, detect_store

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



app = FastAPI()


async def start_parsing_and_callback(data: AskNewItemParse):
    parsed_data = await get_snapshot(data.user_id, data.url, data.source_id)
    async with AsyncClient() as client:
        try:
            if parsed_data is not None:
                response = await client.post(data.callback_url, json=parsed_data.model_dump(mode='json'))
                response.raise_for_status()
                print('\n\nУспешно спарсено, результат отправлен\n\n')
            else:
                raise ValueError(f'Не удалось спарсить карточку (Результат парсинга: None). Карточка: {data.url}')
        except Exception as e:
            error = ParseError(
                source_id=data.source_id,
                url=data.url,
                message=str(e)
            )
            await client.post(data.callback_url + '/error', json=error.model_dump(mode='json'))
            print(f'Не удалось отправить запрос/спарсить данные. Ошибка: {e}')


async def get_snapshot(user_id: int, url: str, source_id: int) -> ItemCreateWithPriceSnapshot | None:
    store_key = detect_store(url)
    if not store_key:
        return None
    parser = get_parser(store_key, headless=True)
    result = await parser.get_product_info(url)
    if result is None or result.get('price') is None:
        return None
    return ItemCreateWithPriceSnapshot(
        user_id=user_id,
        url=url,
        name=result['name'],
        source_id=source_id,
        is_in_stock=True,  # По дефолту True, так оптимистичнее (если есть цена, то, скорее всего, есть и товар)
        price=result['price'],
        currency=result.get('currency') if result.get('currency') else 'RUB',
    )


@app.post('/ask_parse_new_item')
async def start_parsing_new_item(data: AskNewItemParse, background_tasks: BackgroundTasks):
    background_tasks.add_task(start_parsing_and_callback, data)
    # Теперь задача выполняется в фоне, а мы отвечаем беку, что она успешно принята к выполнению
    return {
        'status': 'processing'
    }
