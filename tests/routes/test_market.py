from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_main():
    mock_market_id = "BTC-CLP"
    response = client.get(f"/spreads/{mock_market_id}")
    assert response.status_code == 200
