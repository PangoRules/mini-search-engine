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
