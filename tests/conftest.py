import pytest
from fastapi.testclient import TestClient
from src.mini_search.api import app

@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)