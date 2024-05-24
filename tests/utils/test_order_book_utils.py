from app.utils.order_book_utils import get_min_ask, get_max_bid
from tests.mocks.market_mock import ORDER_BOOK_MOCK


def test_get_min_ask_returns_minimum_ask_price():
    expected_min_ask = 836677.14
    asks = ORDER_BOOK_MOCK["order_book"]["asks"]
    min_ask = get_min_ask(asks)
    assert min_ask == expected_min_ask


def test_get_min_ask_should_fail():
    wrong_min_ask = 837462.23
    asks = ORDER_BOOK_MOCK["order_book"]["asks"]
    min_ask = get_min_ask(asks)
    assert min_ask != wrong_min_ask


def test_get_max_bid_returns_maximum_bid_price():
    expected_max_bid = 821580.0
    bids = ORDER_BOOK_MOCK["order_book"]["bids"]
    max_bid = get_max_bid(bids)
    assert max_bid == expected_max_bid


def test_get_max_bid_should_fail():
    wrong_max_bid = 821211.0
    bids = ORDER_BOOK_MOCK["order_book"]["bids"]
    max_bid = get_max_bid(bids)
    assert max_bid != wrong_max_bid
