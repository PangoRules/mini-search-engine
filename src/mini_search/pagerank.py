import sqlite3
from mini_search.storage.connection import get_connection
from mini_search.storage.scraped_pages import retrieve_scraped_pages
from mini_search.models import ScrapedPage

def _load_pages(conn: sqlite3.Connection) -> list[ScrapedPage]:
    """Paginated loop to retrieve all pages."""
    pages, skip = [], 0
    while True:
        batch = retrieve_scraped_pages(conn, skip=skip, take=100)
        if not batch:
            break
        pages.extend(batch)
        skip += 100
    return pages

def _build_graph(pages: list[ScrapedPage]) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    """Returns (out_links, in_links) — both keyed by page_id, values are lists of page_ids."""
    url_to_id = {page.url: page.id for page in pages}
    
    # initialize empty lists for all nodes
    out_links = {page.id: [] for page in pages}
    in_links  = {page.id: [] for page in pages}
    
    for page in pages:
        for link_url in page.links:
            if link_url in url_to_id and url_to_id[link_url] != page.id:
                target_id = url_to_id[link_url]
                if target_id not in out_links[page.id]:  # deduplicate
                    out_links[page.id].append(target_id)
                    in_links[target_id].append(page.id)
    
    return out_links, in_links

def compute_pagerank(conn: sqlite3.Connection, d=0.85, max_iter=100, tol=1e-6) -> dict[int, float]:
    """Compute PageRank scores for all scraped pages."""
    pages = _load_pages(conn)
    N = len(pages)
    out_links, in_links = _build_graph(pages)
    all_ids = [p.id for p in pages]
    
    scores = {pid: 1.0 / N for pid in all_ids}
    
    for _ in range(max_iter):
        dangling_sum = sum(scores[pid] for pid in all_ids if len(out_links[pid]) == 0)
        
        new_scores = {}
        for pid in all_ids:
            rank = (1 - d) / N + d * (dangling_sum / N)
            for src in in_links[pid]:
                rank += d * (scores[src] / len(out_links[src]))
            new_scores[pid] = rank
        
        delta = max(abs(new_scores[pid] - scores[pid]) for pid in all_ids)
        scores = new_scores
        if delta < tol:
            break
    
    total = sum(scores.values())
    return {pid: s / total for pid, s in scores.items()}

def main():
    """Test the PageRank implementation."""
    with get_connection() as conn:
        scores = compute_pagerank(conn)
    for pid, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        print(f"page_id={pid}  pagerank={score:.6f}")

if __name__ == "__main__":
    main()