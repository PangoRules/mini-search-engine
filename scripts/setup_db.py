from sqlite3 import Connection
from mini_search.storage.documents import create_documents_table, clear_documents_table
from mini_search.storage.connection import get_connection
from mini_search.storage.document_tokens import (
    create_document_tokens_table,
    clear_documents_tokens_table,
)
from mini_search.storage.scraped_pages import (
    clear_scraped_pages_table,
    create_scraped_pages_table,
)
from mini_search.storage.scraped_page_tokens import (
    clear_scraped_page_tokens_table,
    create_scraped_page_tokens_table,
)


def clean_up_documents(conn: Connection) -> None:
    clear_documents_table(conn)
    clear_documents_tokens_table(conn)
    clear_scraped_pages_table(conn)
    clear_scraped_page_tokens_table(conn)


def main() -> None:
    with get_connection() as conn:
        clearAnswer = input("Do you want to clear the db? (y/n)")
        if clearAnswer.lower() == "y":
            clean_up_documents(conn)
        try:
            create_documents_table(conn)
            create_document_tokens_table(conn)
            create_scraped_pages_table(conn)
            create_scraped_page_tokens_table(conn)
            print("Database initialized.")
        except:
            print("Database initialization unsucessful.")
            raise


if __name__ == "__main__":
    main()
