from typing import Optional, Union
from app.routes.messages import (
    SUCCESSFUL_SAVE_ALERT_MESSAGE,
    UNSUCCESSFUL_SAVE_ALERT_MESSAGE,
)
from app.routes.models import (
    ErrorResponse,
    MarketSpreadAlertResponse,
    MarketSpreadsResponse,
    SpreadResponse,
    SpreadResponseWithAlert,
)
from fastapi import APIRouter, status, HTTPException, Path, Query
from app.services.spread_service import (
    calculate_spread,
    get_market_spread_alerts,
    obtain_markets_spread,
)
from app.utils.errors import (
    INTERNAL_SERVER_ERROR_MESSAGE,
    NOT_FOUND_ERROR_MESSAGE,
    OrderBookNotFoundError,
    SpreadAlertNotFoundError,
)

router = APIRouter()


@router.get(
    "/spreads/{market_id}",
    responses={
        200: {
            "model": Union[SpreadResponse, SpreadResponseWithAlert],
            "description": "Successful response",
        },
        404: {"model": ErrorResponse, "description": NOT_FOUND_ERROR_MESSAGE},
        500: {"model": ErrorResponse, "description": INTERNAL_SERVER_ERROR_MESSAGE},
    },
    tags=["Spread"],
    summary="Market spread",
)
async def get_market_spread(
    market_id: str = Path(..., example="btc-clp"),
    set_alert: Optional[bool] = Query(False, alias="setAlert"),
) -> Union[SpreadResponse, SpreadResponseWithAlert]:
    """
    Retrieve the spread for a specific market given the market ID.

    Parameters:
    - **market_id** [string]: The ID of the market to calculate the spread.
    - **setAlert** [boolean]: Optional boolean to set an alert for the market spread.

    Returns:
    - **spread** [float]: The calculated spread for the market.
    - **alert_message** [string, Optional]: A message indicating whether setting the alert was successful (only if **setAlert** is True).
    """
    try:
        if set_alert:
            spread, set_alert_successful = await calculate_spread(
                market_id.lower(), set_alert
            )
        else:
            spread = await calculate_spread(market_id.lower())
    except OrderBookNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_ERROR_MESSAGE
        )
    except Exception as e:
        print("Raising exc:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MESSAGE,
        )

    if not set_alert:
        return SpreadResponse(spread=spread)
    if set_alert_successful:
        return SpreadResponseWithAlert(
            spread=spread, alert_message=SUCCESSFUL_SAVE_ALERT_MESSAGE
        )
    return SpreadResponseWithAlert(
        spread=spread, alert_message=UNSUCCESSFUL_SAVE_ALERT_MESSAGE
    )


@router.get(
    "/spreads",
    responses={
        200: {
            "model": MarketSpreadsResponse,
            "description": "Successful response",
        },
        500: {"model": ErrorResponse, "description": INTERNAL_SERVER_ERROR_MESSAGE},
    },
    tags=["Spread"],
    summary="All markets spread",
)
async def get_all_markets_spreads() -> MarketSpreadsResponse:
    """
    Calculates the spread for all available markets.

    Returns:
    - **spreads** [object]: Object containing all the available markets spreads
        - **{market_id}** [float]: Indicates the spread for the respective {market_id}
    """
    try:
        markets_spread = await obtain_markets_spread()
        return markets_spread
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MESSAGE,
        )


@router.get(
    "/spreads/{market_id}/alert",
    responses={
        200: {
            "model": MarketSpreadAlertResponse,
            "description": "Successful response",
        },
        404: {"model": ErrorResponse, "description": NOT_FOUND_ERROR_MESSAGE},
        500: {"model": ErrorResponse, "description": INTERNAL_SERVER_ERROR_MESSAGE},
    },
    tags=["Spread"],
    summary="Get market spread alert",
)
async def get_market_spread_alert(
    market_id: str = Path(..., example="btc-clp"),
) -> MarketSpreadAlertResponse:
    """
    Retrieves a previously saved maket spread alert.

    Parameters:
    - **market_id** [string]: The ID of the market to retrieve alert.

    Returns:
    - **market_id** [string]: The ID of the market of the retrieved alert.
    - **spread** [float]: The spread of the alert saved for the corresponding market.
    """
    try:
        market_spread_data = get_market_spread_alerts(market_id)
        return market_spread_data
    except SpreadAlertNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_ERROR_MESSAGE
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MESSAGE,
        )
