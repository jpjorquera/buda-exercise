from app.repositories.market_repository import get_order_book
from app.utils.order_book_utils import get_min_ask, get_max_bid


async def calculate_spread(market_id: str) -> float:
    try:
        order_book = get_order_book(market_id)
        asks = order_book["asks"]
        bids = order_book["bids"]
        min_ask = get_min_ask(asks)
        max_bid = get_max_bid(bids)
        spread = min_ask - max_bid
        return spread
    except Exception as e:
        raise e
