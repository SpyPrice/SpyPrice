from http import HTTPStatus

from fastapi import HTTPException, status

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_current_user, get_async_session
from app.schemas import UserRead, ItemCreate, WatchResponse, ItemCreateWithPriceSnapshot

from app.services import cards as cards_service


router = APIRouter()


@router.post('/add_watch_item', tags=['cards', 'safe'], response_model=WatchResponse)
async def add_watch(
        item: ItemCreate,
        db: AsyncSession = Depends(get_async_session),
        current_user: UserRead = Depends(get_current_user)
    ):
    result = await cards_service.add_watch(str(item.source_url), current_user.id, db)
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
            status_code=HTTPStatus.CONFLICT,
            detail='Карточка уже отслеживается'
        )
    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Не удалось добавить карточку'
    )


@router.post('/webhook/etl-add-item-parse-result', include_in_schema=False)
async def parse_result(
        card: ItemCreateWithPriceSnapshot,
        db: AsyncSession = Depends(get_async_session)
):
    try:
        card_id = await cards_service.create_card_and_watch(
            user_id=card.user_id,
            url=card.url,
            name=card.name,
            is_in_stock=card.is_in_stock,
            source_id=card.source_id,
            db=db
        )

        await cards_service.create_price_snapshot(
            item_id=card_id,
            price=card.price,
            currency=card.currency,
            db=db
        )
        return status.HTTP_200_OK

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error: {e}'
        )
