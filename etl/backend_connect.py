from httpx import AsyncClient
import asyncio
from fastapi import FastAPI, BackgroundTasks


app = FastAPI()


async def start_parsing_and_callback(data):
    parsed_data = ... # Здесь будет логика запуска парсинга
    print('\n'*5, 'ВСЁ РАБОТАЕТ', '\n'*5)
    async with AsyncClient() as client:
        try:
            response = await client.post(data.callback_url, json=parsed_data)  # Заменить отправляемый тип данных на тот, что реализует Эдик
            response.raise_for_status()
        except Exception as e:
            print(f'Не удалось отправить запрос. Ошибка: {e}')


@app.post('/ask_parse_new_item')
async def start_parsing_new_item(data: dict, background_tasks: BackgroundTasks):  # Заменить получаем тип данных на тот, что реализует Эдик
    background_tasks.add_task(start_parsing_and_callback, data)
    # Теперь задача выполняется в фоне, а мы отвечаем беку, что она успешно принята к выполнению
    return {
        'status': 'processing'
    }
