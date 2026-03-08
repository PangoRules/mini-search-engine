from mini_search.config import SAMPLE_DOCS_DIR
from mini_search.models import Document
from mini_search.storage import insert_documents, get_connection


def get_files_found() -> list[Document]:
    documents: list[Document] = []
    for file_path in SAMPLE_DOCS_DIR.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")
        documents.append(
            Document(path=str(file_path), title=file_path.stem, content=content)
        )
    return documents


def main() -> None:
    with get_connection() as conn:
        documents = get_files_found()
        insert_documents(conn, documents)


if __name__ == "__main__":
    main()
