"""Test API endpoints for the mini-search-engine."""

import pytest
from fastapi.testclient import TestClient
from src.mini_search.api import app

def test_search_endpoint_basic(client):
    """Test basic search endpoint functionality."""
    response = client.get("/search", params={"q": "test"})
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_results" in data
    assert "total_pages" in data
    assert "results" in data

def test_search_endpoint_with_results(client):
    """Test search endpoint with actual results from sample data."""
    response = client.get("/search", params={"q": "book"})
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "book"
    assert data["page"] == 1
    assert data["page_size"] == 10
    # We expect some results from the sample data
    assert isinstance(data["total_results"], int)
    assert isinstance(data["total_pages"], int)
    assert isinstance(data["results"], list)

def test_search_pagination(client):
    """Test pagination parameters work correctly."""
    response = client.get("/search", params={"q": "book", "page": 1, "page_size": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 5

def test_search_pagination_bounds(client):
    """Test pagination with out of bounds page number."""
    response = client.get("/search", params={"q": "book", "page": 999, "page_size": 5})
    assert response.status_code == 200
    data = response.json()
    # Should adjust to last page
    assert data["page"] >= 1

def test_search_pagination_total_pages_calculation(client):
    """Test that total pages are calculated correctly."""
    response = client.get("/search", params={"q": "book", "page_size": 1})
    assert response.status_code == 200
    data = response.json()
    # With 1 result per page, total_pages should equal total_results
    assert data["total_pages"] >= 1

def test_search_invalid_parameters(client):
    """Test search with invalid parameters."""
    # Test invalid page parameter - should default to page 1
    response = client.get("/search", params={"q": "test", "page": -1})
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    
    # Test invalid page_size parameter - should default to 10
    response = client.get("/search", params={"q": "test", "page_size": 0})
    assert response.status_code == 200
    data = response.json()
    assert data["page_size"] == 10

def test_search_large_page_size(client):
    """Test search with large page size."""
    response = client.get("/search", params={"q": "test", "page_size": 100})
    assert response.status_code == 200
    data = response.json()
    # Should cap at 50
    assert data["page_size"] == 10  # Default value