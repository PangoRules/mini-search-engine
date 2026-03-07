from mini_search.storage import create_documents_table, get_connection


def main() -> None:
    with get_connection() as conn:
        try:
            create_documents_table(conn)
            print("Database initialized.")
        except:
            print("Database initialization unsucessful.")
            raise


if __name__ == "__main__":
    main()
