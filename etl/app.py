import os
import re
import time
from datetime import datetime, timezone
from typing import Any

import httpx
from bs4 import BeautifulSoup

API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000")
ETL_API_KEY = os.getenv("ETL_API_KEY", "change-me-etl-key")
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
FETCH_DELAY_SECONDS = float(os.getenv("FETCH_DELAY_SECONDS", "1"))

HEADERS = {
    "User-Agent": "PriceTrackerBot/1.0 (+educational project)",
    "Accept-Language": "ru,en;q=0.9",
}


def extract_price_dns(html: str) -> tuple[str | None, str]:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    match = re.search(r"(\d[\d\s]{2,})\s?[₽р]", text)
    if not match:
        return None, "RUB"
    value = re.sub(r"\s+", "", match.group(1))
    return f"{int(value):.2f}", "RUB"


def extract_price_ozon(html: str) -> tuple[str | None, str]:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    match = re.search(r"(\d[\d\s]{2,})\s?[₽р]", text)
    if not match:
        return None, "RUB"
    value = re.sub(r"\s+", "", match.group(1))
    return f"{int(value):.2f}", "RUB"


def safe_fetch(url: str) -> str:
    last_error = ""
    for attempt in range(MAX_RETRIES):
        try:
            with httpx.Client(timeout=REQUEST_TIMEOUT_SECONDS, follow_redirects=True, headers=HEADERS) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.text
        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
            sleep_sec = 2**attempt
            time.sleep(sleep_sec)
    raise RuntimeError(last_error)


def post_snapshot(payload: dict[str, Any]) -> None:
    with httpx.Client(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        response = client.post(
            f"{API_BASE_URL}/api/v1/price-snapshots/internal",
            json=payload,
            headers={"X-ETL-API-Key": ETL_API_KEY},
        )
        response.raise_for_status()


def collect_once(product_id: str, source: str, url: str) -> None:
    fetched_at = datetime.now(timezone.utc).isoformat()
    try:
        html = safe_fetch(url)
        if source == "dns_html":
            price, currency = extract_price_dns(html)
        elif source == "ozon_html":
            price, currency = extract_price_ozon(html)
        else:
            raise ValueError(f"Unsupported source: {source}")

        if price is None:
            payload = {
                "product_id": product_id,
                "price": "0.00",
                "currency": "RUB",
                "fetched_at": fetched_at,
                "status": "error",
                "error_message": "price_not_found",
                "availability": "unknown",
                "raw_data": {"source": source},
            }
        else:
            payload = {
                "product_id": product_id,
                "price": price,
                "currency": currency,
                "fetched_at": fetched_at,
                "status": "success",
                "error_message": None,
                "availability": "unknown",
                "raw_data": {"source": source},
            }
        post_snapshot(payload)
    except Exception as exc:  # noqa: BLE001
        error_payload = {
            "product_id": product_id,
            "price": "0.00",
            "currency": "RUB",
            "fetched_at": fetched_at,
            "status": "error",
            "error_message": str(exc)[:500],
            "availability": "unknown",
            "raw_data": {"source": source, "url": url},
        }
        post_snapshot(error_payload)
    finally:
        time.sleep(FETCH_DELAY_SECONDS)


if __name__ == "__main__":
    demo_items = os.getenv("DEMO_ITEMS", "")
    if not demo_items:
        print("Set DEMO_ITEMS as product_id|parser_type|url;product_id|parser_type|url")
        raise SystemExit(1)

    for row in demo_items.split(";"):
        product_id, parser_type, url = row.split("|", maxsplit=2)
        collect_once(product_id.strip(), parser_type.strip(), url.strip())
    print("ETL run completed")
