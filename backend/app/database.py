from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


# В дальнейшем нужно получать из ENV
DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/price_tracker'
engine = create_async_engine(
    DATABASE_URL,
    echo=True,          # вывод в консоль запросов к db
    pool_pre_ping=True, # проверка перед подключением
)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


class Base(DeclarativeBase):
    pass
