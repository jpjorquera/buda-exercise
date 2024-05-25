MARKET_ID_MOCK = "btc-clp"
INVALID_MARKET_ID_MOCK = "123-456"

ORDER_BOOK_MOCK = {
    "order_book": {
        "asks": [
            ["836677.14", "0.447349"],
            ["837462.23", "1.43804963"],
            ["837571.89", "1.41498541"],
        ],
        "bids": [
            ["821580.0", "0.25667389"],
            ["821211.0", "0.27827307"],
            ["819882.39", "1.40003128"],
        ],
    }
}

ORDER_BOOK_NO_SPREAD_MOCK = {
    "order_book": {
        "asks": [
            ["836677.14", "0.447349"],
            ["837462.23", "1.43804963"],
            ["837571.89", "1.41498541"],
        ],
        "bids": [
            ["836677.14", "0.25667389"],
            ["821211.0", "0.27827307"],
            ["819882.39", "1.40003128"],
        ],
    }
}

ORDER_BOOK_WITH_BID_HIGHER_THAN_ASK_MOCK = {
    "order_book": {
        "asks": [
            ["836677.14", "0.447349"],
            ["837462.23", "1.43804963"],
            ["837571.89", "1.41498541"],
        ],
        "bids": [
            ["836678.14", "0.25667389"],
            ["821211.0", "0.27827307"],
            ["819882.39", "1.40003128"],
        ],
    }
}

EMPTY_ORDER_BOOK_MOCK = {
    "order_book": {
        "asks": [],
        "bids": [],
    }
}

MARKETS_MOCK = {
    "markets": [
        {
            "id": "BTC-CLP",
            "name": "btc-clp",
            "base_currency": "BTC",
            "quote_currency": "CLP",
            "minimum_order_amount": ["0.001", "BTC"],
            "taker_fee": "0.8",
            "maker_fee": "0.4",
            "max_orders_per_minute": 100,
            "maker_discount_percentage": "0.0",
            "taker_discount_percentage": "0.0",
        },
        {
            "id": "BTC-COP",
            "name": "btc-cop",
            "base_currency": "BTC",
            "quote_currency": "COP",
            "minimum_order_amount": ["0.001", "BTC"],
            "taker_fee": "0.8",
            "maker_fee": "0.4",
            "max_orders_per_minute": 100,
            "maker_discount_percentage": "0.0",
            "taker_discount_percentage": "0.0",
        },
    ]
}
