from fastapi import HTTPException, status

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_current_user, get_async_session
from app.schemas import UserRead, ItemCreate, WatchResponse, ItemRead, ItemStatistic, PriceStatistics

from app.services import cards as cards_service


import asyncio
from app.services import loop as parsers_loop


router = APIRouter()


@router.post('/cards/add_watch_item', tags=['cards', 'safe'], response_model=WatchResponse)
async def add_watch(
        item: ItemCreate,
        db: AsyncSession = Depends(get_async_session),
        current_user: UserRead = Depends(get_current_user)
    ):
    try:
        result = await cards_service.add_watch(str(item.source_url), current_user.id, item.tags, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.INTERNAL_SERVER_ERROR,
            detail='Непредвиденная ошибка на сервере при добавлении карточки'
        )
    if result == 'success':
        return WatchResponse(
            status='success',
            message='Карточка успешно добавлена к отслеживанию'
        )
    elif result == 'pending':
        return WatchResponse(
            status='pending',
            message='Начало добавления карточки. Старт ETL'
        )
    elif result == 'already_watched':
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Карточка уже отслеживается'
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Не удалось добавить карточку'
    )


@router.get('/cards/get_all_watch_items', tags=['cards', 'safe'], response_model=list[ItemRead])
async def get_all_watch_items_with_snapshots(
        db: AsyncSession = Depends(get_async_session),
        current_user: UserRead = Depends(get_current_user)
):
    user_cards = await cards_service.get_all_users_cards_with_snapshots(current_user.id, db)
    return user_cards


@router.get('/cards/card_info', tags=['cards'], response_model=ItemStatistic)
async def get_card_info(
        card_id: int,
        db: AsyncSession = Depends(get_async_session)):

    item = await cards_service.generate_item_read(card_id, db)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    all_price_snapshots = await cards_service.get_all_snapshots(card_id, db)

    statistics = await cards_service.get_price_statistics(all_price_snapshots)

    return ItemStatistic(
        item=item,
        statistics=statistics,
        update_history=all_price_snapshots
    )


@router.post(
    '/cards/start_parse_loop',
    tags=['cards', 'backend'],
    description='''
    Очень тестовая штука. Как остановить - я пока хз. Он запарсит все карточки и сам остановится на 3 часа.
    Запускать осторожно, не спеша, черемша.
    При запуске на сервере должен быть выключен VPN, чтобы не банили ip для парсинга.
    Советую запускать НЕ через ручку, а напрямую из кода:
    Из /SpyPrice/backend>     python -m app.services.loop 
    ''',
    include_in_schema=True
)
async def start_parse_loop():
    asyncio.create_task(parsers_loop.start_loop())
