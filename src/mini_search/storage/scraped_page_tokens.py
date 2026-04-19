import sqlite3
from collections import Counter, defaultdict

from mini_search.models import ScrapedPage
from mini_search.storage.connection import get_connection
from mini_search.tokenizer import tokenize
from mini_search.storage.scraped_pages import retrieve_scraped_pages


def create_scraped_page_tokens_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
     CREATE TABLE IF NOT EXISTS scraped_page_tokens (
          scraped_page_id INTEGER NOT NULL,
          token TEXT NOT NULL,
          frequency INTEGER NOT NULL,
          UNIQUE(scraped_page_id, token),
          FOREIGN KEY (scraped_page_id) REFERENCES scraped_pages(id)
         )
     """)
    conn.commit()


def clear_scraped_page_tokens_table(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        DELETE FROM scraped_page_tokens;
     """)
    conn.commit()


def flatten_tokens_from_scraped_page(scraped_page: ScrapedPage) -> list[str]:
    tokens: list[str] = []

    # title: list[str]
    if scraped_page.title:
        tokens.extend(scraped_page.title)

    # meta_description: plain str — only field that needs tokenize()
    if scraped_page.meta_description:
        tokens.extend(tokenize(scraped_page.meta_description))

    # headings: dict[str, list[list[str]]]
    if scraped_page.headings:
        for token_lists in scraped_page.headings.values():
            for token_list in token_lists:
                tokens.extend(token_list)

    # paragraphs: list[list[str]]
    if scraped_page.paragraphs:
        for token_list in scraped_page.paragraphs:
            tokens.extend(token_list)

    # links: list[str] — URLs, skip

    # images: list[dict] with optional "altTokens": list[str]
    if scraped_page.images:
        for image in scraped_page.images:
            if "altTokens" in image:
                tokens.extend(image["altTokens"])

    # lists: list[list[list[str]]]
    if scraped_page.lists:
        for list_group in scraped_page.lists:
            for list_item in list_group:
                tokens.extend(list_item)

    # tables: list[dict] with "headersTag": list[list[str]] and "tableDataTag": list[list[list[str]]]
    if scraped_page.tables:
        for table in scraped_page.tables:
            for token_list in table.get("headersTag", []):
                tokens.extend(token_list)
            for row in table.get("tableDataTag", []):
                for token_list in row:
                    tokens.extend(token_list)

    return tokens


def insert_scraped_page_idx_entries(
    conn: sqlite3.Connection, tokenDict: dict[str, dict[int, int]]
) -> None:
    rows = []
    for token, pages in tokenDict.items():
        for page, freq in pages.items():
            rows.append((page, token, freq))
    try:
        conn.executemany(
            """
            INSERT INTO scraped_page_tokens (scraped_page_id, token, frequency)
            VALUES (?, ?, ?)
        """,
            rows,
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print("Some of the relations already exist.")


def build_scraped_pages_inverted_index(conn: sqlite3.Connection) -> None:
    inverted_index: dict[str, dict[int, int]] = defaultdict(dict)
    batch_size = 100
    skip = 0

    while True:
        scraped_pages = retrieve_scraped_pages(conn, skip=skip, take=batch_size)
        if not scraped_pages:
            break

        for page in scraped_pages:
            if page.id is None:
                continue
            tokens = flatten_tokens_from_scraped_page(page)
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                inverted_index[token][page.id] = count

        skip += batch_size

    if inverted_index:
        insert_scraped_page_idx_entries(conn, inverted_index)


def main():
    with get_connection() as conn:
        clear_scraped_page_tokens_table(conn)
        build_scraped_pages_inverted_index(conn)


if __name__ == "__main__":
    main()
