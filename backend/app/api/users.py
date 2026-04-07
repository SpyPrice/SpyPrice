from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..schemas import UserCreate, UserRead

from ..services import users as users_repository

router = APIRouter()


@router.post("/users", tags=["users"], response_model=UserRead)
async def create_user(new_user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    return await users_repository.create_user(db, new_user.email, new_user.name, new_user.password)


