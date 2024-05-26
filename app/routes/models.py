from app.routes.messages import SUCCESSFUL_SAVE_ALERT_MESSAGE
from pydantic import BaseModel, Field
from typing import Optional


class SpreadResponse(BaseModel):
    spread: float = Field(..., example=15179.14)
    alert_message: Optional[str] = Field(..., example=SUCCESSFUL_SAVE_ALERT_MESSAGE)


class ErrorResponse(BaseModel):
    detail: str


class MarketSpreadsResponse(BaseModel):
    spreads: dict = Field(..., example={"BTC-CLP": 100, "BTC-COP": 2000, "ETH-CLP": 0})


class MarketSpreadAlertResponse(BaseModel):
    market_id: str = Field(..., example="btc-clp")
    spread: float = Field(..., example=1000.15)
