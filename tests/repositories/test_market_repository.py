from app.utils.errors import (
    ExternalAPIError,
    OrderBookNotFoundError,
    SpreadAlertNotFoundError,
)
import pytest
from unittest.mock import patch, Mock, mock_open
from requests.models import Response
from app.repositories.market_repository import (
    ALERTS_FILE_PATH,
    get_all_markets,
    get_order_book,
    retrieve_market_spread_alert,
    save_market_spread_alert,
)
from tests.mocks.market_mock import MARKET_ID_MOCK, MARKETS_MOCK, ORDER_BOOK_MOCK
import json

from tests.mocks.spread_mock import MARKET_SPREAD_ALERT_MOCK


def test_get_order_book_success():
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = ORDER_BOOK_MOCK
    with patch(
        "app.repositories.market_repository.requests.get", return_value=mock_response
    ):
        order_book = get_order_book(MARKET_ID_MOCK)
        assert order_book == mock_response.json()["order_book"]


def test_get_order_book_not_found():
    mock_response = Mock(spec=Response)
    mock_response.status_code = 404
    with patch(
        "app.repositories.market_repository.requests.get", return_value=mock_response
    ):
        with pytest.raises(OrderBookNotFoundError):
            get_order_book(MARKET_ID_MOCK)


def test_get_order_book_unexpected_error():
    mock_response = Mock(spec=Response)
    mock_response.status_code = 500
    with patch(
        "app.repositories.market_repository.requests.get", return_value=mock_response
    ):
        with pytest.raises(ExternalAPIError):
            get_order_book(MARKET_ID_MOCK)


def test_get_all_markets_success():
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = MARKETS_MOCK
    with patch(
        "app.repositories.market_repository.requests.get", return_value=mock_response
    ):
        markets = get_all_markets()
        assert markets == mock_response.json()["markets"]


def test_get_all_markets_unexpected_error():
    mock_response = Mock(spec=Response)
    mock_response.status_code = 500
    with patch(
        "app.repositories.market_repository.requests.get", return_value=mock_response
    ):
        with pytest.raises(ExternalAPIError):
            get_all_markets()


def test_save_market_spread_alert_success():
    mock_alert_data_str = json.dumps(MARKET_SPREAD_ALERT_MOCK)
    mock_spread = 100
    file_open_mock = mock_open(read_data=mock_alert_data_str)
    with patch("builtins.open", file_open_mock):
        save_market_result = save_market_spread_alert(MARKET_ID_MOCK, mock_spread)
        file_open_mock.assert_called_with(
            f"{ALERTS_FILE_PATH}/{MARKET_ID_MOCK}.json", "w"
        )
        assert save_market_result == True


def test_get_market_spread_alert_success():
    mock_alert_data_str = json.dumps(MARKET_SPREAD_ALERT_MOCK)
    file_open_mock = mock_open(read_data=mock_alert_data_str)
    with patch("builtins.open", file_open_mock):
        market_spread_data = retrieve_market_spread_alert(MARKET_ID_MOCK)
        file_open_mock.assert_called_with(
            f"{ALERTS_FILE_PATH}/{MARKET_ID_MOCK}.json", "r"
        )
        assert market_spread_data == MARKET_SPREAD_ALERT_MOCK


def test_get_market_spread_alert_error_when_no_alert_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(SpreadAlertNotFoundError):
            retrieve_market_spread_alert(MARKET_ID_MOCK)
