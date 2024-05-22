from fastapi.testclient import TestClient
from app.routes.spreads import app

client = TestClient(app)

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "Hello world!"