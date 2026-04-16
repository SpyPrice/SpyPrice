from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from app.parsers import get_parser, detect_store
from app.schemas import ItemResponse, ItemRequest
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI(title="Price Parser API")

@app.post("/parse", response_model=ItemResponse) # измени путь, если другой
async def parse_item(request: ItemRequest):
    snapshot = await get_snapshot(
        user_id=request.user_id,
        url=request.url,
        source_id=request.source_id
    )
    if snapshot is None or snapshot.price is None:
        raise HTTPException(status_code=404, detail="Что то пошло не так( мб не та ссылка")
    return snapshot



async def get_snapshot(user_id: int, url: str, source_id: int) -> Optional[ItemResponse]:
    store_key = detect_store(url)
    if not store_key:
        return None
    parser = get_parser(store_key, headless=True)
    result = await parser.get_product_info(url)
    if  result is None or result.get("price") is None:
        return None
    return ItemResponse(
        user_id=user_id,
        url=url,
        name=result["name"],
        source_id=source_id,
        is_in_stock=None,
        price=result["price"],
        currency=result.get("currency", "RUB")
    )