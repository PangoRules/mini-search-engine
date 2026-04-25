import pytest
from mini_search.index_builder import build_inverted_index
from mini_search.models import Document


def test_build_inverted_index_empty():
    """Test building index with empty document list."""
    documents = []
    result = build_inverted_index(documents)
    assert result == {}


def test_build_inverted_index_single_document():
    """Test building index with a single document."""
    doc = Document(path="/test/path", title="Test Title", content="hello world", id=1)
    documents = [doc]
    result = build_inverted_index(documents)
    
    assert "hello" in result
    assert "world" in result
    assert 1 in result["hello"]
    assert 1 in result["world"]
    assert result["hello"][1] == 1
    assert result["world"][1] == 1


def test_build_inverted_index_multiple_documents():
    """Test building index with multiple documents."""
    doc1 = Document(path="/test/path1", title="Test Title 1", content="hello world", id=1)
    doc2 = Document(path="/test/path2", title="Test Title 2", content="hello moon", id=2)
    documents = [doc1, doc2]
    
    result = build_inverted_index(documents)
    
    assert "hello" in result
    assert "world" in result
    assert "moon" in result
    
    # Check document IDs
    assert 1 in result["hello"]
    assert 2 in result["hello"]
    assert 1 in result["world"]
    assert 2 in result["moon"]
    
    # Check frequencies
    assert result["hello"][1] == 1
    assert result["hello"][2] == 1
    assert result["world"][1] == 1
    assert result["moon"][2] == 1


def test_build_inverted_index_with_duplicates():
    """Test building index with duplicate terms in document."""
    doc = Document(path="/test/path", title="Test Title", content="hello hello world world", id=1)
    documents = [doc]
    
    result = build_inverted_index(documents)
    
    assert "hello" in result
    assert "world" in result
    
    assert 1 in result["hello"]
    assert 1 in result["world"]
    
    # Check frequencies (should be 2 for hello, 2 for world)
    assert result["hello"][1] == 2
    assert result["world"][1] == 2


def test_build_inverted_index_with_stopwords():
    """Test building index with stopwords in documents."""
    doc = Document(path="/test/path", title="Test Title", content="the quick brown fox jumps over the lazy dog", id=1)
    documents = [doc]
    
    result = build_inverted_index(documents)
    
    # Stopwords should be removed
    assert "the" not in result
    assert "over" not in result
    
    # Non-stopwords should be present
    assert "quick" in result
    assert "brown" in result
    assert "fox" in result
    assert "jumps" in result
    assert "lazy" in result
    assert "dog" in result