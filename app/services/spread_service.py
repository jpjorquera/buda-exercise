from typing import Tuple, Union
from app.repositories.market_repository import (
    get_all_markets,
    get_order_book,
    retrieve_market_spread_alert,
    save_market_spread_alert,
)
from app.utils.order_book_utils import get_min_ask, get_max_bid


async def calculate_spread(
    market_id: str, set_alert: bool = False
) -> Union[float, Tuple[float, bool]]:
    try:
        order_book = get_order_book(market_id)
        asks = order_book["asks"]
        bids = order_book["bids"]

        if not asks or not bids:
            return None

        min_ask = get_min_ask(asks)
        max_bid = get_max_bid(bids)
        spread = min_ask - max_bid
        spread = round(spread, 2)
    except Exception as e:
        raise e

    if set_alert:
        set_alert_successful = save_market_spread_alert(market_id, spread)
        return spread, set_alert_successful
    return spread


async def obtain_markets_spread():
    try:
        markets = get_all_markets()
        markets_ids = [market["id"] for market in markets]
        markets_spread = dict()
        for market_id in markets_ids:
            markets_spread[market_id] = await calculate_spread(market_id)
        return {"spreads": markets_spread}
    except Exception as e:
        raise e


def get_market_spread_alerts(market_id: str):
    try:
        spread_data = retrieve_market_spread_alert(market_id)
        return spread_data
    except Exception as e:
        raise e
