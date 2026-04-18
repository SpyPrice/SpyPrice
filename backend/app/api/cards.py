from http import HTTPStatus

from fastapi import HTTPException, status

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_current_user, get_async_session
from app.schemas import UserRead, ItemCreate, WatchResponse, ItemCreateWithPriceSnapshot, ItemRead, ParseError

from app.services import cards as cards_service


router = APIRouter()


@router.post('/cards/add_watch_item', tags=['cards', 'safe'], response_model=WatchResponse)
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


@router.get('/cards/get_all_watch_items', tags=['cards', 'safe'], response_model=list[ItemRead])
async def get_all_watch_items_with_snapshots(
        db: AsyncSession = Depends(get_async_session),
        current_user: UserRead = Depends(get_current_user)
):
    user_cards = await cards_service.get_all_users_cards_with_snapshots(current_user.id, db)
    return user_cards

