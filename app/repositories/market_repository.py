import requests
import json
import os
from app.repositories import API_BASE_URL
from app.utils.errors import (
    ExternalAPIError,
    OrderBookNotFoundError,
    SpreadAlertNotFoundError,
)

ALERTS_FILE_PATH = "./spread_alerts"


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


def save_market_spread_alert(market_id: str, alert_spread: float) -> bool:
    market_spread_alert_file = f"{ALERTS_FILE_PATH}/{market_id}.json"
    spread_data = {"market_id": market_id, "spread": alert_spread}
    successful_save = False
    os.makedirs(ALERTS_FILE_PATH, exist_ok=True)
    try:
        with open(market_spread_alert_file, "w") as file:
            json.dump(spread_data, file)
        successful_save = True
    except Exception as e:
        print(e)
        return successful_save
    return successful_save


def retrieve_market_spread_alert(market_id: str) -> dict:
    market_spread_alert_file = f"{ALERTS_FILE_PATH}/{market_id}.json"
    try:
        with open(market_spread_alert_file, "r") as file:
            market_spread_data = json.load(file)
            return market_spread_data
    except FileNotFoundError:
        raise SpreadAlertNotFoundError(market_id)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
