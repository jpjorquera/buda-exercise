from app.routes.spread_routes import (
    SUCCESSFUL_SAVE_ALERT_MESSAGE,
)
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

MOCK_CALCULATE_SPREAD_RESPONSE = 100, None
MOCK_CALCULATE_SPREAD_RESPONSE_WITH_SUCCESSFUL_ALERT = 100, True

client = TestClient(app)


def test_get_market_spread_success():
    with patch(
        "app.routes.spread_routes.calculate_spread",
        return_value=MOCK_CALCULATE_SPREAD_RESPONSE,
    ):
        response = client.get(f"/spreads/{MARKET_ID_MOCK}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "spread": MOCK_CALCULATE_SPREAD_RESPONSE[0],
            "alert_message": MOCK_CALCULATE_SPREAD_RESPONSE[1],
        }


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


def test_get_market_spread_with_alert_success():
    with patch(
        "app.routes.spread_routes.calculate_spread",
        return_value=MOCK_CALCULATE_SPREAD_RESPONSE_WITH_SUCCESSFUL_ALERT,
    ):
        response = client.get(f"/spreads/{MARKET_ID_MOCK}?setAlert=True")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "spread": MOCK_CALCULATE_SPREAD_RESPONSE_WITH_SUCCESSFUL_ALERT[0],
            "alert_message": SUCCESSFUL_SAVE_ALERT_MESSAGE,
        }
