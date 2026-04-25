import pytest
from mini_search.utils.url_utils import normalize_url, is_valid_url


def test_is_valid_url_valid_http():
    """Test that valid HTTP URLs are recognized as valid."""
    assert is_valid_url("http://example.com") == True


def test_is_valid_url_valid_https():
    """Test that valid HTTPS URLs are recognized as valid."""
    assert is_valid_url("https://example.com") == True


def test_is_valid_url_invalid_scheme():
    """Test that URLs with invalid schemes are recognized as invalid."""
    assert is_valid_url("ftp://example.com") == False


def test_is_valid_url_no_netloc():
    """Test that URLs with no netloc are recognized as invalid."""
    assert is_valid_url("http://") == False
    assert is_valid_url("https://") == False


def test_is_valid_url_empty_string():
    """Test that empty strings are recognized as invalid."""
    assert is_valid_url("") == False


def test_is_valid_url_none():
    """Test that None values are recognized as invalid."""
    assert is_valid_url(None) == False


def test_normalize_url_basic():
    """Test basic URL normalization."""
    result = normalize_url("https://example.com")
    expected = "https://example.com"
    assert result == expected


def test_normalize_url_with_port():
    """Test URL normalization with port numbers."""
    result = normalize_url("https://example.com:8080/path")
    expected = "https://example.com/path"
    assert result == expected


def test_normalize_url_case_insensitive():
    """Test that URL normalization is case insensitive."""
    result = normalize_url("HTTPS://EXAMPLE.COM/PATH")
    expected = "https://example.com/path"
    assert result == expected


def test_normalize_url_with_query_params():
    """Test URL normalization with query parameters."""
    result = normalize_url("https://example.com/path?b=2&a=1")
    expected = "https://example.com/path?a=1&b=2"
    assert result == expected


def test_normalize_url_with_fragment():
    """Test URL normalization with fragments."""
    result = normalize_url("https://example.com/path#section")
    expected = "https://example.com/path"
    assert result == expected


def test_normalize_url_path_case():
    """Test that path is normalized to lowercase."""
    result = normalize_url("https://example.com/Path")
    expected = "https://example.com/path"
    assert result == expected


def test_normalize_url_path_strips_slash():
    """Test that leading and trailing slashes are stripped from paths."""
    result = normalize_url("https://example.com/path/")
    expected = "https://example.com/path"
    assert result == expected


def test_normalize_url_with_base():
    """Test URL normalization with base URL."""
    result = normalize_url("/relative", "https://example.com/base")
    expected = "https://example.com/relative"
    assert result == expected


def test_normalize_url_invalid_url():
    """Test that invalid URLs raise ValueError."""
    with pytest.raises(ValueError):
        normalize_url("invalid-url")