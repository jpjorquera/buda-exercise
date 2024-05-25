from app.utils.errors import (
    ExternalAPIError,
    OrderBookNotFoundError,
)
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from tests.mocks.market_mock import INVALID_MARKET_ID_MOCK, MARKET_ID_MOCK
from tests.mocks.spread_mock import MARKETS_SPREAD_MOCK

MOCK_SPREAD = 100

client = TestClient(app)


def test_get_market_spread_success():
    with patch("app.routes.spread_routes.calculate_spread", return_value=MOCK_SPREAD):
        response = client.get(f"/spreads/{MARKET_ID_MOCK}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"spread": MOCK_SPREAD}


def test_get_market_spread_should_throw_not_found_when_there_is_no_order():
    with patch(
        "app.routes.spread_routes.calculate_spread",
        side_effect=OrderBookNotFoundError(INVALID_MARKET_ID_MOCK),
    ):
        response = client.get(f"/spreads/{INVALID_MARKET_ID_MOCK}")
        assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_market_spread_should_throw_internal_error_when_an_error_occurs():
    with patch(
        "app.routes.spread_routes.calculate_spread", side_effect=ExternalAPIError
    ):
        response = client.get(f"/spreads/{MARKET_ID_MOCK}")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_get_all_markets_spreads_success():
    with patch(
        "app.routes.spread_routes.obtain_markets_spread",
        return_value=MARKETS_SPREAD_MOCK,
    ):
        response = client.get("/spreads")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == MARKETS_SPREAD_MOCK


def test_get_all_markets_spreads_should_throw_internal_error_when_an_error_occurs():
    with patch(
        "app.routes.spread_routes.calculate_spread", side_effect=ExternalAPIError
    ):
        response = client.get(f"/spreads/{MARKET_ID_MOCK}")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
