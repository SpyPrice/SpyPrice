from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.cards import router as cards_router


app = FastAPI()
app.include_router(users_router)
app.include_router(cards_router)
