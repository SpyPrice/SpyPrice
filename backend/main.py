from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.cards import router as cards_router
from app.api.backend_etl_api_connect import router as backend_etl_api_connect_router
from app.api.metadata import router as metadata_router

from os import getenv
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

cors_origins_str = getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000')
cors_origins = [origin.strip() for origin in cors_origins_str.split(',')]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(users_router)
app.include_router(cards_router)
app.include_router(backend_etl_api_connect_router)
app.include_router(metadata_router)
