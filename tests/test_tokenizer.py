import pytest
from mini_search.tokenizer import tokenize


def test_tokenize_basic():
    """Test basic tokenization functionality."""
    text = "Hello, World!"
    result = tokenize(text)
    expected = ["hello", "world"]
    assert result == expected


def test_tokenize_with_stopwords():
    """Test tokenization with stopwords removal."""
    text = "This is a test sentence with some stopwords"
    result = tokenize(text)
    # Stopwords should be removed
    assert "this" not in result
    assert "is" not in result
    assert "a" not in result
    assert "with" not in result
    assert "some" not in result
    assert "stopwords" in result
    assert "test" in result
    assert "sentence" in result


def test_tokenize_empty_string():
    """Test tokenization with empty string."""
    result = tokenize("")
    assert result == []


def test_tokenize_punctuation():
    """Test tokenization with various punctuation."""
    text = "Hello!!! How are you??? I'm fine..."
    result = tokenize(text)
    expected = ["hello", "im", "fine"]
    assert result == expected


def test_tokenize_numbers():
    """Test tokenization with numbers."""
    text = "I have 3 apples and 5 oranges"
    result = tokenize(text)
    expected = ["3", "apples", "5", "oranges"]
    assert result == expected


def test_tokenize_case_insensitive():
    """Test that tokenization is case insensitive."""
    text = "Hello HELLO Hello"
    result = tokenize(text)
    expected = ["hello", "hello", "hello"]
    assert result == expected