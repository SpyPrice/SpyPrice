from os import getenv

from httpx import AsyncClient
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import AskNewItemParse, ItemCreateWithPriceSnapshot, ParseError, AskExistsItemParse, \
    PriceSnapshotCreate
from app.services import cards as cards_service
from app.dependency import get_async_session


router = APIRouter()


@router.post('/webhook/etl_add_item_parse_result', tags=['back'], include_in_schema=False)
async def parse_new_item_result(
        card: ItemCreateWithPriceSnapshot,
        db: AsyncSession = Depends(get_async_session)
):
    try:
        await cards_service.change_card_name_and_stock_from_default(
            item_id=card.item_id,
            name=card.name,
            is_in_stock=card.is_in_stock,
            db=db
        )

        await cards_service.create_price_snapshot(
            item_id=card.item_id,
            price=card.price,
            currency=card.currency,
            db=db
        )
        return {
            'status': status.HTTP_200_OK
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error: {e}'
        )


@router.post('/webhook/error', tags=['back'], include_in_schema=False)
async def parse_error_result(error: ParseError):
    print(f'\n\nНе удалось спарсить с источника номер {error.source_id}, url: {error.url}\nОшибка: {error.message}\n\n')


@router.post('/cards/parse_item', tags=['back'], include_in_schema=True)
async def parse_item(
        item_id: int,
        db: AsyncSession = Depends(get_async_session),
):
    card = await cards_service.get_card_by_id(item_id, db)
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    url = card.url
    source_id = card.source_id

    await notify_etl_to_parse_exists_item(item_id, url, source_id)
    return {
        'status': status.HTTP_200_OK
    }


@router.post('/webhook/etl_exists_item_parse_result', tags=['back'], include_in_schema=False)
async def parse_item_exists_result(
        snapshot: PriceSnapshotCreate,
        db: AsyncSession = Depends(get_async_session),
):
    result = await cards_service.create_price_snapshot(
        item_id=snapshot.tracking_item_id,
        price=snapshot.price,
        currency=snapshot.currency,
        db=db
    )
    return {
        'status': status.HTTP_200_OK
    }


async def notify_etl_to_parse_exists_item(item_id: int, url: str, source_id: int):
    etl_base_url = getenv('ETL_URL', 'http://127.0.0.1:8080')
    backend_base_url = getenv('API_BASE_URL', 'http://127.0.0.1:8000')

    etl_url = f'{etl_base_url}/ask_parse_exists_item'
    callback_url = f'{backend_base_url}/webhook/etl_exists_item_parse_result'

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


async def notify_etl_to_parse_new_item(item_id: int, url: str, source_id: int):
    etl_base_url = getenv('ETL_URL', 'http://127.0.0.1:8080')
    backend_base_url = getenv('API_BASE_URL', 'http://127.0.0.1:8000')

    etl_url = f'{etl_base_url}/ask_parse_new_item'
    callback_url = f'{backend_base_url}/webhook/etl_add_item_parse_result'

    print(f'Отправляем в etl new_item_(который теперь уже есть в бд, надо только ему имя обновить) {url=}')
    async with AsyncClient() as client:
        try:
            result = await client.post(etl_url, json=AskNewItemParse(
                url=url,
                item_id=item_id,
                source_id=source_id,
                callback_url=callback_url
            ).model_dump())
            result.raise_for_status()
        except Exception as e:
            print('\n'*3 + f'ошибка связи с ETL: {e}' + '\n'*3)
