from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserCreate, UserRead, Token, TokenWithUser
from app.services import users as users_service
from app.security import create_access_token
from app.dependency import get_current_user, get_async_session

router = APIRouter()


@router.post('/register', tags=['users'], response_model=TokenWithUser)
async def create_user(new_user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    user = await users_service.create_user(db, new_user.email, new_user.name, new_user.password)
    access_token = create_access_token(data={'sub': str(user.id)})
    return TokenWithUser(
        access_token=access_token,
        token_type='bearer',
        user=UserRead.model_validate(user)
    )


@router.get('/me', tags=['users'], response_model=UserRead)
async def get_me(current_user: UserRead = Depends(get_current_user)):
    return current_user


@router.post('/login', tags=['users'], response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_async_session)
    ):
    user = await users_service.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    access_token = create_access_token(data = {'sub': str(user.id)})
    return Token(
        access_token=access_token,
        token_type='bearer'
    )
