MARKETS_SPREAD_MOCK = {
    "spreads": {
        "BTC-CLP": 15097.14,
        "BTC-COP": None,
    }
}


async def mock_calculate_spread(market_id: str):
    return MARKETS_SPREAD_MOCK["spreads"][market_id]
