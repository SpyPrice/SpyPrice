from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models import User
from app.repository import users as users_repository


def _hash_password(password: str) -> str:
    return ''.join(chr(ord(i) + 1) for i in password)


def _verify_password(check_password, hashed_password) -> bool:
    return _hash_password(check_password) == hashed_password


async def create_user(db: AsyncSession, email: str, name: str, password: str) -> User:
    if await users_repository.get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail='User already exists. Email is taken.')

    user = await users_repository.create_user(db, email, name, _hash_password(password))
    await db.commit()
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    user = await users_repository.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=400, detail='User does not exist.')
    elif not _verify_password(password, user.password):
        raise HTTPException(status_code=400, detail='Invalid password or email.')

    return user
