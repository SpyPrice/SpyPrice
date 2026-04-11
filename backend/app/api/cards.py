from fastapi import HTTPException, status

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency import get_current_user, get_async_session
from app.schemas import UserRead, ItemCreate, WatchResponse

from app.services import cards as cards_repository


router = APIRouter()


@router.post('/add_watch_item', tags=['cards'], response_model=WatchResponse)
async def add_watch(
        item: ItemCreate,
        db: AsyncSession = Depends(get_async_session),
        current_user: UserRead = Depends(get_current_user)
    ):
    result = await cards_repository.add_watch(str(item.source_url), current_user.id, db)
    if result:
        return WatchResponse(
            status='success',
            message='Карточка успешно добавлена к отслеживанию'
        )
    elif result is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Карточка уже отслеживается'
        )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='Не удалось добавить карточку'
    )
