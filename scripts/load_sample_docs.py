from sqlite3 import Connection
from mini_search.config import SAMPLE_DOCS_DIR
from mini_search.models import Document
from mini_search.storage.connection import get_connection
from mini_search.storage.documents import insert_documents


def get_files_found() -> list[Document]:
    documents: list[Document] = []
    for file_path in SAMPLE_DOCS_DIR.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")
        documents.append(
            Document(path=str(file_path), title=file_path.stem, content=content)
        )
    return documents


def load_docs(conn: Connection) -> None:
    documents = get_files_found()
    insert_documents(conn, documents)


def main() -> None:
    with get_connection() as conn:
        load_docs(conn)


if __name__ == "__main__":
    main()
