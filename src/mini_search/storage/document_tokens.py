import sqlite3

from mini_search.storage.connection import get_connection


def create_document_tokens_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
     CREATE TABLE IF NOT EXISTS document_tokens (
          doc_id INTEGER NOT NULL,
          token TEXT NOT NULL,
          frequency INTEGER NOT NULL,
          UNIQUE(doc_id,token)
         )
     """)
    conn.commit()


def clear_documents_tokens_table(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        DELETE FROM document_tokens;
     """)
    conn.commit()


def insert_idx_entries(
    conn: sqlite3.Connection, tokenDict: dict[str, dict[int, int]]
) -> None:
    rows = []
    for token, docs in tokenDict.items():
        for doc, freq in docs.items():
            rows.append((doc, token, freq))
    try:
        conn.executemany(
            """
            INSERT INTO document_tokens (doc_id, token, frequency)
            VALUES (?, ?, ?)
        """,
            rows,
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print("Some of the relations already exist.")


def fetch_idx_entries(conn: sqlite3.Connection, tokens: list[str]) -> dict[int, int]:
    placeholders = ", ".join("?" for _ in tokens)
    cursor = conn.execute(
        f"""
            SELECT doc_id, token, frequency
            FROM document_tokens
            WHERE token IN ({placeholders})
        """,
        tokens,
    )
    rawResults = cursor.fetchall()

    results = {}
    for row in rawResults:
        doc_id = row["doc_id"]
        results[doc_id] = results.get(doc_id, 0) + row["frequency"]

    return results


def main():
    with get_connection() as conn:
        print(fetch_idx_entries(conn, ["python", "sqlite", "indexes"]))


if __name__ == "__main__":
    main()
