from httpx import AsyncClient
from fastapi import FastAPI, BackgroundTasks

from etl.app.schemas import AskNewItemParse, AskExistsItemParse, ItemCreateWithPriceSnapshot, ParseError, ParseResult, \
    PriceSnapshotCreate

from etl.app.choose_parser import get_parser, detect_store

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI()


async def start_parsing_new_item_and_callback(data: AskNewItemParse):
    parsed_data = await get_snapshot(data.url)

    async with AsyncClient() as client:
        try:
            if parsed_data is not None:
                to_send_data = ItemCreateWithPriceSnapshot(
                    item_id=data.item_id,
                    url=data.url,
                    name=parsed_data.name,
                    source_id=data.source_id,
                    is_in_stock=True,
                    # По дефолту True, так оптимистичнее (если есть цена, то, скорее всего, есть и товар)
                    price=parsed_data.price,
                    currency=parsed_data.currency,
                )
                response = await client.post(data.callback_url, json=to_send_data.model_dump(mode='json'))
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
            error_url = data.callback_url[:data.callback_url.find('/webhook')] + '/webhook/error'
            await client.post(error_url, json=error.model_dump(mode='json'))
            print(f'Не удалось отправить запрос/спарсить данные. Ошибка: {e}')


async def start_parsing_exists_item_and_callback(data: AskExistsItemParse):
    parsed_data = await get_snapshot(data.url)

    async with AsyncClient() as client:
        try:
            if parsed_data is not None:
                to_send_data = PriceSnapshotCreate(
                    tracking_item_id=data.item_id,
                    price=parsed_data.price,
                    currency=parsed_data.currency,
                )
                response = await client.post(data.callback_url, json=to_send_data.model_dump(mode='json'))
                response.raise_for_status()

                print('\n\nУспешно спарсено, результат отправлен\n\n')
            else:
                raise ValueError(
                    f'Не удалось спарсить карточку (Результат парсинга: None). Карточка: {data.item_id=} {data.url=}')
        except Exception as e:
            error = ParseError(
                source_id=data.source_id,
                url=data.url,
                message=str(e)
            )
            error_url = data.callback_url[:data.callback_url.find('/webhook')] + '/webhook/error'
            await client.post(error_url, json=error.model_dump(mode='json'))
            print(f'Не удалось отправить запрос/спарсить данные. Ошибка: {e}')


async def get_snapshot(url: str) -> ParseResult | None:
    store_key = detect_store(url)
    if not store_key:
        return None
    parser = get_parser(store_key, headless=True)
    result = await parser.get_product_info(url)
    if result is None or result.get('price') is None:
        return None

    return ParseResult(
        name=result['name'],
        price=result['price'],
        currency=result.get('currency') if result.get('currency') else 'RUB'
    )


@app.post('/ask_parse_new_item')
async def start_parsing_new_item(data: AskNewItemParse, background_tasks: BackgroundTasks):
    background_tasks.add_task(start_parsing_new_item_and_callback, data)
    # Теперь задача выполняется в фоне, а мы отвечаем беку, что она успешно принята к выполнению
    return {
        'status': 'processing'
    }


@app.post('/ask_parse_exists_item')
async def start_parsing_exists_item(data: AskExistsItemParse, background_tasks: BackgroundTasks):
    background_tasks.add_task(start_parsing_exists_item_and_callback, data)
    # Теперь задача выполняется в фоне, а мы отвечаем беку, что она успешно принята к выполнению
    return {
        'status': 'processing'
    }
