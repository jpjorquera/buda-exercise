from app.utils.errors import ExternalAPIError, OrderBookNotFoundError
import pytest
from unittest.mock import patch, Mock
from requests.models import Response
from app.repositories.market_repository import get_order_book
from tests.mocks.market_mock import MARKET_ID_MOCK, ORDER_BOOK_MOCK


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
