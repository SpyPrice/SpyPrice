from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.database import async_session_maker
from app.security import SECRET_KEY, ALGORITHM
from app.schemas import UserRead
from app.repository import users as users_repository


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


async def get_current_user(
    db: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme)
) -> UserRead:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials.',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get('sub'))
        user = await users_repository.get_user_by_id(db, user_id)
        if not user:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    except ValueError:

        credentials_exception.detail += 'ID must be an integer'
        raise credentials_exception

    return UserRead.model_validate(user)
