from fastapi import APIRouter, status, HTTPException
from app.services.market_service import calculate_spread
from app.utils.errors import (
    INTERNAL_SERVER_ERROR_MESSAGE,
    NOT_FOUND_ERROR_MESSAGE,
    OrderBookNotFoundError,
)

router = APIRouter()


@router.get("/markets/{market_id}/spread")
async def get_market_spread(market_id: str):
    try:
        spread = await calculate_spread(market_id)
        return {"spread": spread}
    except OrderBookNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_ERROR_MESSAGE
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=INTERNAL_SERVER_ERROR_MESSAGE,
        )
