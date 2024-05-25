import uvicorn
from fastapi import FastAPI
from app.routes import spread_routes

app = FastAPI()
app.include_router(spread_routes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
