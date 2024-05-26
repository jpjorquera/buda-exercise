import pytest
from unittest.mock import patch
from app.services.spread_service import (
    calculate_spread,
    get_market_spread_alerts,
    obtain_markets_spread,
)
from app.utils.errors import ExternalAPIError
from tests.mocks.market_mock import (
    EMPTY_ORDER_BOOK_MOCK,
    MARKET_ID_MOCK,
    ORDER_BOOK_MOCK,
    ORDER_BOOK_NO_SPREAD_MOCK,
    ORDER_BOOK_WITH_BID_HIGHER_THAN_ASK_MOCK,
    MARKETS_MOCK,
)
from tests.mocks.spread_mock import (
    MARKET_SPREAD_ALERT_MOCK,
    MARKETS_SPREAD_MOCK,
    mock_calculate_spread,
)


@pytest.mark.asyncio
async def test_calculate_spread_success():
    expected_spread = 15097.14
    with patch(
        "app.services.spread_service.get_order_book",
        return_value=ORDER_BOOK_MOCK["order_book"],
    ):
        spread, alert_message = await calculate_spread(MARKET_ID_MOCK)
        assert spread == expected_spread


@pytest.mark.asyncio
async def test_calculate_spread_error():
    with patch(
        "app.services.spread_service.get_order_book",
        side_effect=ExternalAPIError,
    ):
        with pytest.raises(ExternalAPIError):
            await calculate_spread(MARKET_ID_MOCK)


@pytest.mark.asyncio
async def test_calculate_spread_success_with_no_spread():
    expected_spread = 0
    with patch(
        "app.services.spread_service.get_order_book",
        return_value=ORDER_BOOK_NO_SPREAD_MOCK["order_book"],
    ):
        spread, alert_message = await calculate_spread(MARKET_ID_MOCK)
        assert spread == expected_spread


@pytest.mark.asyncio
async def test_calculate_spread_success_with_negative_spread():
    expected_spread = -1.0
    with patch(
        "app.services.spread_service.get_order_book",
        return_value=ORDER_BOOK_WITH_BID_HIGHER_THAN_ASK_MOCK["order_book"],
    ):
        spread, alert_message = await calculate_spread(MARKET_ID_MOCK)
        assert spread == expected_spread


@pytest.mark.asyncio
async def test_calculate_returns_none_with_empty_order_book():
    expected_spread = None
    with patch(
        "app.services.spread_service.get_order_book",
        return_value=EMPTY_ORDER_BOOK_MOCK["order_book"],
    ):
        spread = await calculate_spread(MARKET_ID_MOCK)
        assert spread == expected_spread


@pytest.mark.asyncio
async def test_obtain_markets_spread_success():
    with patch(
        "app.services.spread_service.get_all_markets",
        return_value=MARKETS_MOCK["markets"],
    ):
        with patch(
            "app.services.spread_service.calculate_spread",
            side_effect=mock_calculate_spread,
        ):
            markets_spread = await obtain_markets_spread()
            assert markets_spread == MARKETS_SPREAD_MOCK


@pytest.mark.asyncio
async def test_obtain_markets_spread_error():
    with patch(
        "app.services.spread_service.get_all_markets",
        side_effect=ExternalAPIError,
    ):
        with pytest.raises(ExternalAPIError):
            await obtain_markets_spread()


@pytest.mark.asyncio
async def test_calculate_spread_with_alert():
    expected_spread = 15097.14
    expected_set_alert_status = True
    with patch(
        "app.services.spread_service.get_order_book",
        return_value=ORDER_BOOK_MOCK["order_book"],
    ):
        with patch(
            "app.services.spread_service.save_market_spread_alert",
            return_value=True,
        ):
            spread, alert_status = await calculate_spread(
                MARKET_ID_MOCK, set_alert=True
            )
            assert spread == expected_spread
            assert alert_status == expected_set_alert_status


def test_get_market_spread_alerts_success():
    with patch(
        "app.services.spread_service.retrieve_market_spread_alert",
        return_value=MARKET_SPREAD_ALERT_MOCK,
    ):
        result = get_market_spread_alerts(MARKET_ID_MOCK)
        assert result == MARKET_SPREAD_ALERT_MOCK


def test_get_market_spread_alerts_error():
    with patch(
        "app.services.spread_service.retrieve_market_spread_alert",
        side_effect=FileNotFoundError,
    ):
        with pytest.raises(FileNotFoundError):
            get_market_spread_alerts(MARKET_ID_MOCK)
