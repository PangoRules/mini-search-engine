import threading
import time
from collections import defaultdict
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from urllib.parse import quote

from mini_search.search_scraped_pages import search_with_authority
from mini_search.storage.scraped_pages import fetch_paragraphs_by_ids
from mini_search.storage.connection import get_connection

app = FastAPI(title="Mini Search Engine API")

# Rate limiting implementation
# Sliding window with timestamps list per IP
_rate_store: Dict[str, List[float]] = defaultdict(list)
_rate_lock = threading.Lock()
_MAX_REQUESTS = 10
_WINDOW_SECONDS = 60

def is_rate_limited(client_ip: str) -> bool:
    """Check if client is rate limited."""
    current_time = time.time()
    
    with _rate_lock:
        # Clean old requests outside the window
        _rate_store[client_ip] = [
            req_time for req_time in _rate_store[client_ip]
            if current_time - req_time < _WINDOW_SECONDS
        ]
        
        # Check if over limit
        if len(_rate_store[client_ip]) >= _MAX_REQUESTS:
            return True
            
        # Add current request
        _rate_store[client_ip].append(current_time)
        return False

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    score: float

class SearchResponse(BaseModel):
    query: str
    page: int
    page_size: int
    total_results: int
    total_pages: int
    results: List[SearchResult]

@app.get("/search", response_model=SearchResponse)
async def search(request: Request, q: str = Query(min_length=1), page: int = 1, page_size: int = 10):
    """Search endpoint with pagination support."""
    # Rate limiting
    client_ip = request.client.host if request.client else "unknown"
    if is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Too Many Requests")
    
    # Validate parameters
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 50:
        page_size = 10
    
    # Perform search
    all_results = search_with_authority(q)
    
    # Calculate pagination
    total_results = len(all_results)
    total_pages = max(1, (total_results + page_size - 1) // page_size)
    
    # Adjust page if it's out of bounds
    if page > total_pages:
        page = total_pages
    
    # Slice results for current page
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_results = all_results[start_idx:end_idx]
    
    # Fetch paragraphs only for the current page's IDs
    page_ids = [r.page_id for r in paginated_results]
    page_paragraphs = {}
    if page_ids:
        with get_connection() as conn:
            page_paragraphs = fetch_paragraphs_by_ids(conn, page_ids)
    
    # Build response results with snippets
    response_results = []
    for result in paginated_results:
        # Get snippet from first non-empty paragraph
        snippet = ""
        if result.page_id in page_paragraphs:
            for paragraph in page_paragraphs[result.page_id]:
                if paragraph and len(paragraph) > 0:
                    # Join tokens with spaces and take first 30 words
                    snippet = " ".join(paragraph[:30])
                    break
        
        # Handle title - join list with spaces or use fallback
        title = "Untitled"
        if result.title:
            if isinstance(result.title, list):
                title = " ".join(result.title)
            else:
                title = result.title
        
        response_results.append(SearchResult(
            title=title,
            url=result.url,
            snippet=snippet,
            score=round(result.score, 6)
        ))
    
    return SearchResponse(
        query=q,
        page=page,
        page_size=page_size,
        total_results=total_results,
        total_pages=total_pages,
        results=response_results
    )
