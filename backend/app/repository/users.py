from ..database import get_async_session
from ..models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, email: str, name: str, hash_password: str):
    user = User(email=email, name=name, password=hash_password)
    db.add(user)
    await db.flush()
    return user


async def get_user(db: AsyncSession, email: str) -> User | None:
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()
