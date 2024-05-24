PRICE_POSITION = 0


def get_max_bid(bids: list) -> float:
    max_bid_order = max(bids, key=lambda order: float(order[PRICE_POSITION]))
    max_bid = float(max_bid_order[PRICE_POSITION])
    return max_bid


def get_min_ask(asks: list) -> float:
    min_ask_order = min(asks, key=lambda order: float(order[PRICE_POSITION]))
    min_ask = float(min_ask_order[PRICE_POSITION])
    return min_ask
