from mini_search.storage.documents import create_documents_table
from mini_search.storage.connection import get_connection
from mini_search.storage.document_tokens import create_document_tokens_table


def main() -> None:
    with get_connection() as conn:
        try:
            create_documents_table(conn)
            create_document_tokens_table(conn)
            print("Database initialized.")
        except:
            print("Database initialization unsucessful.")
            raise


if __name__ == "__main__":
    main()
