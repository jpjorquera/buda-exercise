import requests

from app.repositories import API_BASE_URL
from app.utils.errors import ExternalAPIError, OrderBookNotFoundError


def get_order_book(market_id: str) -> dict:
    order_book_url = f"{API_BASE_URL}/markets/{market_id}/order_book"
    response = requests.get(order_book_url)
    if response.status_code == 404:
        raise OrderBookNotFoundError(market_id)
    if response.status_code != 200:
        raise ExternalAPIError
    return response.json()["order_book"]


def get_all_markets() -> list:
    markets_url = f"{API_BASE_URL}/markets"
    response = requests.get(markets_url)
    if response.status_code != 200:
        raise ExternalAPIError
    return response.json()["markets"]
