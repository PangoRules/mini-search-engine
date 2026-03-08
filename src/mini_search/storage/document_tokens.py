import sqlite3


def create_document_tokens_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
     CREATE TABLE IF NOT EXISTS document_tokens (
          doc_id INTEGER NOT NULL,
          token TEXT NOT NULL,
          UNIQUE(doc_id,token)
         )
     """)
    conn.commit()
