from fastapi import FastAPI
from app.routes import market_routes

app = FastAPI()
app.include_router(market_routes.router)
