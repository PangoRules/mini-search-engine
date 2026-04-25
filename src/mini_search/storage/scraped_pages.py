import sqlite3
import json

from mini_search.models import ScrapedPage
from mini_search.utils.scrape_utils import ScrapedPageDto


def create_scraped_pages_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
     CREATE TABLE IF NOT EXISTS scraped_pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            meta_description TEXT NULL,
            headings TEXT NOT NULL,
            paragraphs TEXT NOT NULL,
            links TEXT NOT NULL,
            images TEXT NOT NULL,
            lists TEXT NOT NULL,
            tables TEXT NOT NULL
         )
     """)
    conn.commit()


def clear_scraped_pages_table(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        DELETE FROM scraped_pages;
        DELETE FROM sqlite_sequence WHERE name='scraped_pages';
     """)
    conn.commit()


def insert_scraped_page(conn: sqlite3.Connection, dto: ScrapedPageDto) -> None:
    conn.execute(
        """
             INSERT INTO scraped_pages
             (url, title, meta_description, headings, paragraphs, links, images, lists, tables) VALUES
             (?, ?, ?, ?, ?, ?, ? ,? ,?)
        """,
        (
            dto["url"],
            json.dumps(dto["title"]) if dto["title"] else None,
            dto["meta_description"],
            json.dumps(dto["headings"]),
            json.dumps(dto["paragraphs"]),
            json.dumps(dto["links"]),
            json.dumps(dto["images"]),
            json.dumps(dto["lists"]),
            json.dumps(dto["tables"]),
        ),
    )
    conn.commit()


def retrieve_scraped_pages(
    conn: sqlite3.Connection, skip: int = 0, take: int = 10
) -> list[ScrapedPage]:
    scrapedPages = conn.execute(
        """
                SELECT 
                    id, url, title, meta_description, headings, paragraphs, links, images, lists, tables
                FROM scraped_pages LIMIT ? OFFSET ?
            """,
        (take, skip),
    )

    return list(map(map_raw_scraped_to_dto, scrapedPages))


def fetch_paragraphs_by_ids(conn: sqlite3.Connection, page_ids: list[int]) -> dict[int, list[list[str]]]:
    """Fetch paragraphs for given page IDs.
    
    Args:
        conn: Database connection
        page_ids: List of page IDs to fetch
        
    Returns:
        Dict mapping page_id to list of paragraph tokens
    """
    if not page_ids:
        return {}
    
    # Create placeholders for the IN clause
    placeholders = ','.join('?' * len(page_ids))
    
    query = f"""
    SELECT id, paragraphs FROM scraped_pages WHERE id IN ({placeholders})
    """
    
    cursor = conn.cursor()
    cursor.execute(query, page_ids)
    rows = cursor.fetchall()
    
    result = {}
    for row in rows:
        page_id = row["id"]
        # Parse the JSON paragraphs field
        paragraphs = json.loads(row["paragraphs"]) if row["paragraphs"] else []
        result[page_id] = paragraphs
    
    return result


def map_raw_scraped_to_dto(raw_doc):
    return ScrapedPage(
        raw_doc["url"],
        raw_doc["title"],
        raw_doc["meta_description"],
        raw_doc["headings"],
        raw_doc["paragraphs"],
        raw_doc["links"],
        raw_doc["images"],
        raw_doc["lists"],
        raw_doc["tables"],
        raw_doc["id"],
    )
