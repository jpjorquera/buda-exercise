from fastapi import FastAPI
from app.routes import market

app = FastAPI()
app.include_router(market.router)
