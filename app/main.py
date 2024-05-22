from fastapi import FastAPI
from app.routes import spreads

app = FastAPI()
app.include_router(spreads.router)