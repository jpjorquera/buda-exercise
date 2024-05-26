from typing import Optional
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
from pydantic import BaseModel, Field

router = APIRouter()

SUCCESSFUL_SAVE_ALERT_MESSAGE = "Alert saved successfully"
UNSUCCESSFUL_SAVE_ALERT_MESSAGE = "We were unable to save the alert"


class SpreadResponse(BaseModel):
    spread: float = Field(..., example=15179.14)
    alert_message: Optional[str] = Field(..., example=SUCCESSFUL_SAVE_ALERT_MESSAGE)


class ErrorResponse(BaseModel):
    detail: str


class MarketSpreadsResponse(BaseModel):
    spreads: dict = Field(..., example={"BTC-CLP": 100, "BTC-COP": 2000, "ETH-CLP": 0})


@router.get(
    "/spreads/{market_id}",
    response_model=Optional[SpreadResponse],
    responses={
        404: {"model": ErrorResponse, "description": NOT_FOUND_ERROR_MESSAGE},
        500: {"model": ErrorResponse, "description": INTERNAL_SERVER_ERROR_MESSAGE},
    },
    tags=["Spread"],
    summary="Market spread",
    description="Given a market ID, this endpoint retrieves the \
                order book and calculates the spread.",
)
async def get_market_spread(
    market_id: str = Path(..., example="btc-clp"),
    set_alert: Optional[bool] = Query(False, alias="setAlert"),
) -> SpreadResponse:
    try:
        spread, set_alert_successful = await calculate_spread(
            market_id.lower(), set_alert
        )
    except OrderBookNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_ERROR_MESSAGE
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MESSAGE,
        )

    if not set_alert:
        return SpreadResponse(spread=spread, alert_message=None)
    if set_alert_successful:
        return SpreadResponse(
            spread=spread, alert_message=SUCCESSFUL_SAVE_ALERT_MESSAGE
        )
    return SpreadResponse(spread=spread, alert_message=UNSUCCESSFUL_SAVE_ALERT_MESSAGE)


@router.get(
    "/spreads",
    response_model=MarketSpreadsResponse,
    responses={
        500: {"model": ErrorResponse, "description": INTERNAL_SERVER_ERROR_MESSAGE},
    },
    tags=["Spread"],
    summary="All markets spread",
    description="Calculates the spread for all available markets.",
)
async def get_all_markets_spreads() -> MarketSpreadsResponse:
    try:
        markets_spread = await obtain_markets_spread()
        return markets_spread
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MESSAGE,
        )


@router.get("/spreads/{market_id}/alert")
async def get_market_spread_alert(
    market_id: str = Path(..., example="btc-clp"),
):
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
