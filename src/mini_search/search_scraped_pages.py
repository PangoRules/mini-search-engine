import sqlite3
import math
import json
from dataclasses import dataclass

from mini_search.tokenizer import tokenize
from mini_search.storage.connection import get_connection

# Import PageRank functionality
from mini_search.pagerank import compute_pagerank

@dataclass
class SearchResult:
    page_id: int
    url: str
    title: str
    score: float

def _fetch_token_data(conn: sqlite3.Connection, tokens: list[str]) -> list[sqlite3.Row]:
    """Fetch all token data for query terms in one shot."""
    # Create placeholders for the IN clause
    placeholders = ','.join('?' * len(tokens))
    
    query = f"""
    SELECT spt.scraped_page_id, spt.token, spt.frequency,
           totals.total_tokens,
           n.doc_count
    FROM scraped_page_tokens spt
    JOIN (
        SELECT scraped_page_id, SUM(frequency) AS total_tokens
        FROM scraped_page_tokens GROUP BY scraped_page_id
    ) AS totals ON spt.scraped_page_id = totals.scraped_page_id
    JOIN (SELECT COUNT(DISTINCT id) AS doc_count FROM scraped_pages) AS n ON 1=1
    WHERE spt.token IN ({placeholders})
    """
    
    cursor = conn.cursor()
    cursor.execute(query, tokens)
    return cursor.fetchall()

def _fetch_page_metadata(conn: sqlite3.Connection, page_ids: list[int]) -> dict[int, tuple[str, str]]:
    """Fetch page metadata for matched IDs."""
    if not page_ids:
        return {}
        
    # Create placeholders for the IN clause
    placeholders = ','.join('?' * len(page_ids))
    
    query = f"""
    SELECT id, url, title FROM scraped_pages WHERE id IN ({placeholders})
    """
    
    cursor = conn.cursor()
    cursor.execute(query, page_ids)
    rows = cursor.fetchall()
    
    # Convert to dictionary mapping page_id to (url, title)
    metadata = {}
    for row in rows:
        # Handle title being stored as JSON
        title = json.loads(row["title"]) if row["title"] else None
        metadata[row["id"]] = (row["url"], title)
    
    return metadata

def _compute_tfidf_scores(rows: list[sqlite3.Row]) -> dict[int, float]:
    """Compute TF-IDF scores for all pages."""
    if not rows:
        return {}
        
    # Step 1: df(t) from result rows
    # Count distinct scraped_page_id per token
    df_counts = {}
    
    for row in rows:
        token = row["token"]
        if token not in df_counts:
            df_counts[token] = set()
        df_counts[token].add(row["scraped_page_id"])
    
    # Convert sets to counts
    df_counts = {token: len(page_ids) for token, page_ids in df_counts.items()}
    
    # Step 2: N from any row (total number of documents)
    N = rows[0]["doc_count"]
    
    # Step 3: accumulate per page
    scores = {}
    
    for row in rows:
        page_id = row["scraped_page_id"]
        
        # Initialize score for page if not exists
        if page_id not in scores:
            scores[page_id] = 0.0
            
        # Compute TF-IDF score
        tf = row["frequency"] / row["total_tokens"]
        idf = math.log(N / df_counts[row["token"]])
        scores[page_id] += tf * idf
    
    return scores

def search_scraped_pages(query: str) -> list[SearchResult]:
    """Search scraped pages using TF-IDF scoring."""
    if not query:
        raise ValueError("Query string is empty.")
        
    tokens = tokenize(query)
    if not tokens:
        return []
        
    with get_connection() as conn:
        token_rows = _fetch_token_data(conn, tokens)
        if not token_rows:
            return []
            
        scores = _compute_tfidf_scores(token_rows)
        page_ids = list(scores.keys())
        metadata = _fetch_page_metadata(conn, page_ids)
        
        results = [
            SearchResult(page_id=pid, url=metadata[pid][0], title=metadata[pid][1], score=score)
            for pid, score in scores.items()
            if pid in metadata
        ]
        return sorted(results, key=lambda r: r.score, reverse=True)

def search_with_authority(query: str, alpha: float = 0.7) -> list[SearchResult]:
    """Search scraped pages using TF-IDF scoring combined with PageRank authority."""
    tfidf_results = search_scraped_pages(query)
    if not tfidf_results:
        return []
    
    with get_connection() as conn:
        pagerank_scores = compute_pagerank(conn)

    tfidf_map = {r.page_id: r.score for r in tfidf_results}
    
    tfidf_max = max(tfidf_map.values())
    tfidf_norm = {pid: s / tfidf_max for pid, s in tfidf_map.items()}
    
    matched_pr = {pid: pagerank_scores.get(pid, 0.0) for pid in tfidf_map}
    pr_max = max(matched_pr.values()) if any(v > 0 for v in matched_pr.values()) else 1.0
    pr_norm = {pid: s / pr_max for pid, s in matched_pr.items()}
    
    results = [
        SearchResult(
            page_id=pid,
            url=next(r.url for r in tfidf_results if r.page_id == pid),
            title=next(r.title for r in tfidf_results if r.page_id == pid),
            score=alpha * tfidf_norm[pid] + (1 - alpha) * pr_norm[pid],
        )
        for pid in tfidf_map
    ]
    return sorted(results, key=lambda r: r.score, reverse=True)

def main():
    """Test the scorer."""
    results = search_scraped_pages("books")
    for r in results:
        title = " ".join(r.title) if isinstance(r.title, list) else r.title
        print(f"{r.score:.4f}  {title}  {r.url}")

if __name__ == "__main__":
    main()