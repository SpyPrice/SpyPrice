import asyncio
from backend.app.database import engine, Base
from backend.app.models import *


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(init_models())
