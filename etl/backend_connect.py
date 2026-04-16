from httpx import AsyncClient
import asyncio
from fastapi import FastAPI, BackgroundTasks
from decimal import Decimal
from pydantic import BaseModel
from datetime import datetime



class ItemCreateWithPriceSnapshot(BaseModel):   # Временно для норм логики
    user_id: int
    url: str
    name: str
    source_id: int
    is_in_stock: bool | None = None
    price: Decimal
    currency: str


class AskNewItemParse(BaseModel):
    url: str
    user_id: int
    source_id: int
    callback_url: str


app = FastAPI()


async def start_parsing_and_callback(data: AskNewItemParse):
    parsed_data = ItemCreateWithPriceSnapshot(
        url=data.url,
        user_id=data.user_id,
        name='rtx 5060',
        is_in_stock=True,
        price=Decimal(30999),
        source_id=data.source_id,
        currency='RUB',
    ) # Здесь будет логика запуска парсинга

    async with AsyncClient() as client:
        try:
            response = await client.post(data.callback_url, json=parsed_data.model_dump(mode='json'))  # Заменить отправляемый тип данных на тот, что реализует Эдик
            response.raise_for_status()
            print('\n' * 5, 'ВСЁ РАБОТАЕТ', '\n' * 5, datetime.now())
        except Exception as e:
            print(f'Не удалось отправить запрос. Ошибка: {e}')


@app.post('/ask_parse_new_item')
async def start_parsing_new_item(data: AskNewItemParse, background_tasks: BackgroundTasks):  # Заменить получаем тип данных на тот, что реализует Эдик
    background_tasks.add_task(start_parsing_and_callback, data)
    # Теперь задача выполняется в фоне, а мы отвечаем беку, что она успешно принята к выполнению
    return {
        'status': 'processing'
    }
