import sqlite3

from mini_search.storage.connection import get_connection


def create_document_tokens_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
     CREATE TABLE IF NOT EXISTS document_tokens (
          doc_id INTEGER NOT NULL,
          token TEXT NOT NULL,
          UNIQUE(doc_id,token)
         )
     """)
    conn.commit()


def insert_idx_entries(
    conn: sqlite3.Connection, tokenDict: dict[str, set[int]]
) -> None:
    rows = []
    for token, doc_ids in tokenDict.items():
        for doc_id in doc_ids:
            rows.append((doc_id, token))
    try:
        conn.executemany(
            """
            INSERT INTO document_tokens (doc_id, token)
            VALUES (?, ?)
        """,
            rows,
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print("Some of the relations already exist.")


def fetch_idx_entries(conn: sqlite3.Connection, token: str) -> list[int]:
    cursor = conn.execute(
        """
            SELECT doc_id, token
            FROM document_tokens
            WHERE token=?
        """,
        (token,),
    )
    rawResults = cursor.fetchall()

    results = [rawResult["doc_id"] for rawResult in rawResults]

    return results


def main():
    with get_connection() as conn:
        print(fetch_idx_entries(conn, "python"))


if __name__ == "__main__":
    main()
