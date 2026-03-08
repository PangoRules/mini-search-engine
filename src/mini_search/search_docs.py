from mini_search.models import Document
from mini_search.storage.documents import fetch_documents_by_id
from mini_search.tokenizer import tokenize
from mini_search.storage.document_tokens import fetch_idx_entries
from mini_search.storage.connection import get_connection


def search_in_docs(query: str) -> list[Document]:
    if not query:
        raise ValueError("Query string is empty.")

    tokenizedQry = tokenize(query)
    docsFound: list[Document] = []
    with get_connection() as conn:
        idxEntries = fetch_idx_entries(conn, tokenizedQry)
        docIds = [
            idx[0]
            for idx in sorted(idxEntries.items(), key=lambda x: x[1], reverse=True)
        ]
        docsFound = fetch_documents_by_id(conn, docIds)
    return docsFound


def main():
    print(search_in_docs("Python stores"))


if __name__ == "__main__":
    main()
