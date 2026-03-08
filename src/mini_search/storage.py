import sqlite3
from pathlib import Path
from mini_search.config import DB_PATH
from mini_search.models import Document


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_documents_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
     CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            content TEXT NOT NULL
         )
     """)
    conn.commit()


def insert_document(conn: sqlite3.Connection, doc: Document) -> None:
    conn.execute(
        """
         INSERT INTO documents (path, title, content)
         VALUES (?, ?, ?)
        """,
        (doc.path, doc.title, doc.content),
    )
    conn.commit()


def insert_documents(conn: sqlite3.Connection, docs: list[Document]) -> None:
    cursor = conn.cursor()

    parsedDocs = [(obj.path, obj.title, obj.content) for obj in docs]
    try:
        cursor.executemany(
            """
               INSERT INTO documents (path, title, content) VALUES (?, ?, ?)
            """,
            parsedDocs,
        )
        conn.commit()
        print(f"Inserted {len(docs)}")
    except sqlite3.IntegrityError:
        print("Documents already exist in the database.")


def fetch_all_documents(conn: sqlite3.Connection) -> list[Document]:
    cursor = conn.execute("""
                          SELECT id, path, title, content
                          FROM documents
                          ORDER BY id
                          """)
    rawDocs = cursor.fetchall()

    def mapRawResult(rawDoc):
        return Document(rawDoc["path"], rawDoc["title"], rawDoc["content"], rawDoc["id"])

    return list(map(mapRawResult, rawDocs))
