import pytest
from unittest.mock import patch, MagicMock
from mini_search.search_scraped_pages import search_scraped_pages, search_with_authority, _fetch_token_data, _fetch_page_metadata, _compute_tfidf_scores
from mini_search.tokenizer import tokenize


def test_fetch_token_data():
    """Test fetching token data from database."""
    # Mock connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    tokens = ["test", "token"]
    
    # Mock the execute and fetchall methods
    mock_cursor.fetchall.return_value = [
        {"scraped_page_id": 1, "token": "test", "frequency": 2, "total_tokens": 10, "doc_count": 5},
        {"scraped_page_id": 2, "token": "token", "frequency": 1, "total_tokens": 15, "doc_count": 5}
    ]
    
    result = _fetch_token_data(mock_conn, tokens)
    
    # Verify query was called with correct parameters
    mock_cursor.execute.assert_called_once()
    assert len(result) == 2


def test_fetch_page_metadata():
    """Test fetching page metadata from database."""
    # Mock connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    page_ids = [1, 2, 3]
    
    # Mock the execute and fetchall methods
    mock_cursor.fetchall.return_value = [
        {"id": 1, "url": "http://example.com/1", "title": '["Title 1"]'},
        {"id": 2, "url": "http://example.com/2", "title": '["Title 2"]'},
        {"id": 3, "url": "http://example.com/3", "title": '["Title 3"]'}
    ]
    
    result = _fetch_page_metadata(mock_conn, page_ids)
    
    # Verify the result structure
    assert 1 in result
    assert 2 in result
    assert 3 in result
    assert result[1] == ("http://example.com/1", ["Title 1"])
    assert result[2] == ("http://example.com/2", ["Title 2"])
    assert result[3] == ("http://example.com/3", ["Title 3"])


def test_compute_tfidf_scores():
    """Test TF-IDF score computation."""
    # Mock token data rows
    rows = [
        {"scraped_page_id": 1, "token": "test", "frequency": 2, "total_tokens": 10, "doc_count": 5},
        {"scraped_page_id": 1, "token": "token", "frequency": 1, "total_tokens": 10, "doc_count": 5},
        {"scraped_page_id": 2, "token": "test", "frequency": 1, "total_tokens": 15, "doc_count": 5},
    ]
    
    result = _compute_tfidf_scores(rows)
    
    # Should have scores for both pages
    assert 1 in result
    assert 2 in result
    assert isinstance(result[1], float)
    assert isinstance(result[2], float)


def test_search_scraped_pages_empty_query():
    """Test search with empty query."""
    with pytest.raises(ValueError):
        search_scraped_pages("")


def test_search_scraped_pages_no_results():
    """Test search with no matching results."""
    # Mock tokenize to return empty list
    with patch('mini_search.search_scraped_pages.tokenize', return_value=[]):
        result = search_scraped_pages("test")
        assert result == []


def test_search_scraped_pages_with_results():
    """Test search with results (mocked)."""
    # Mock the necessary functions
    with patch('mini_search.search_scraped_pages.tokenize', return_value=["test"]):
        with patch('mini_search.search_scraped_pages._fetch_token_data', return_value=[]):
            with patch('mini_search.search_scraped_pages._fetch_page_metadata', return_value={}):
                with patch('mini_search.search_scraped_pages._compute_tfidf_scores', return_value={}):
                    result = search_scraped_pages("test")
                    assert result == []


def test_search_with_authority():
    """Test search with authority scoring."""
    # Mock the necessary functions
    with patch('mini_search.search_scraped_pages.search_scraped_pages', return_value=[]):
        with patch('mini_search.search_scraped_pages.compute_pagerank', return_value={}):
            result = search_with_authority("test")
            assert result == []