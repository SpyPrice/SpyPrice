from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.cards import router as cards_router
from app.api.backend_etl_api_connect import router as backend_etl_api_connect_router


app = FastAPI()
app.include_router(users_router)
app.include_router(cards_router)
app.include_router(backend_etl_api_connect_router)
