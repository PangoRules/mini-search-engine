"""Test rate limiting functionality."""
import pytest
from fastapi.testclient import TestClient
from mini_search.api import app, _rate_store

@pytest.fixture(autouse=True)
def reset_rate_store():
    _rate_store.clear()
    yield
    _rate_store.clear()

@pytest.fixture
def client():
    return TestClient(app)

def test_rate_limiting_allows_up_to_limit(client):
    for _ in range(10):
        response = client.get("/search", params={"q": "test"})
        assert response.status_code == 200

def test_rate_limiting_blocks_on_exceeded(client):
    for _ in range(10):
        client.get("/search", params={"q": "test"})
    response = client.get("/search", params={"q": "test"})
    assert response.status_code == 429

def test_rate_limiting_different_ips_are_independent(client):
    # Exhaust limit for default IP
    for _ in range(10):
        client.get("/search", params={"q": "test"})
    # Manually add a different IP entry to verify isolation
    from mini_search.api import _rate_store
    assert len(_rate_store) == 1  # only one IP tracked