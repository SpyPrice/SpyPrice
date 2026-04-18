from fastapi import APIRouter, Depends, HTTPException, status

from app.dependency import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import SourceRead, TagRead
from app.services import metadata as metadata_services


router = APIRouter()


@router.get('/metadata/sources', tags=['metadata'], response_model=list[SourceRead])
async def get_all_active_sources(db: AsyncSession = Depends(get_async_session)):
    try:
        sources = await metadata_services.get_all_active_sources(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка: {e}'
        )
    if sources:
        return sources
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='No active sources'
    )


@router.get('/metadata/tags', tags=['metadata'], response_model=list[TagRead])
async def get_all_tags(db: AsyncSession = Depends(get_async_session)):
    try:
        tags = await metadata_services.get_all_tags(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка: {e}'
        )
    if tags:
        return tags
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='No active tags'
    )
