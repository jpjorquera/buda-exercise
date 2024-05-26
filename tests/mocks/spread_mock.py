from tests.mocks.market_mock import MARKET_ID_MOCK


MARKETS_SPREAD_MOCK = {
    "spreads": {
        "BTC-CLP": 15097.14,
        "BTC-COP": None,
    }
}

MARKET_SPREAD_ALERT_MOCK = {"market_id": MARKET_ID_MOCK, "spread": 100}


async def mock_calculate_spread(market_id: str):
    return MARKETS_SPREAD_MOCK["spreads"][market_id]
