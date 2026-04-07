from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from ..schemas import UserRead

from ..repository import users as user_repository


def _hash_password(password: str):
    return ''.join(chr(ord(i) + 1) for i in password)


async def create_user(db: AsyncSession, email: str, name: str, password: str) -> UserRead:
    if await user_repository.get_user(db, email):
        raise HTTPException(status_code=400, detail='User already exists. Email is taken.')

    user = await user_repository.create_user(db, email, name, _hash_password(password))
    await db.commit()
    return UserRead.model_validate(user)




