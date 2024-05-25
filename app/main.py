from fastapi import FastAPI
from app.routes import spread_routes

app = FastAPI()
app.include_router(spread_routes.router)
