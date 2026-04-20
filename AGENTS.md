## Project Setup & Conventions

**Environment:**
*   Use Python 3.14.
*   Dependencies are managed via `pyproject.toml` and installed via `pip install -e .` in the project root.
*   The virtual environment is located at `.venv/`.

**Core Execution Scripts:**
*   **Database Initialization:** Always start by running `python scripts/setup_db.py` to ensure the SQLite schema is correct.
*   **Loading Sample Data:** Use `python scripts/load_sample_docs.py` to populate sample data into the database.
*   **Search:** Run `python src/mini_search/search_docs.py` to search local documents.
*   **Indexing:** Run `python src/mini_search/index_builder.py` to build the inverted index for local documents.
*   **Crawling:** The web crawling process is initiated by running `python src/mini_search/crawler.py`.

## Architecture & Data Flow Quirks

*   **Index Separation:** Maintain strict separation between local document indexing and web crawling indexing.
    *   Local Index: Uses the tables managed by `document_tokens.py`.
    *   Web Index: Uses the tables managed by `scraped_page_tokens.py` (to be implemented in Phase 4).
*   **Web Indexing (Phase 4):**
    *   The pipeline requires extracting tokens **from existing JSON fields** within the `scraped_pages` table.
    *   The raw tokenization step is **already done** when scraping; do not re-tokenize.
    *   The process involves flattening these tokens and performing term frequency counting before storing results in `scraped_page_tokens`.
*   **Search Implementation Details:**
    *   TF-IDF scoring implemented in `search_scraped_pages.py` with proper SQL queries for fetching token data and page metadata.
    *   Uses `mini_search.tokenizer.tokenize()` for consistent tokenization across the application.
    *   Database connections managed via `mini_search.storage.connection.get_connection()` context manager.
    *   Page titles in `scraped_pages` table are stored as JSON arrays and require `json.loads()` processing.
    *   TF-IDF computation includes proper document frequency calculation from query results.
*   **Local Document Indexing:** After loading document samples, indexing is performed by calling `index_builder.py`.
*   **Search Interface:** Search queries are handled by `search_docs.py`.

## Development Workflow

*   **Testing:** Testing occurs via `pytest` in the `tests/` directory. See `phases.md` for test inclusion in Phase 7.
*   **Linting & Formatting:** Lint with `ruff check src/` and format with `black src/`. These are defined in `pyproject.toml`.
*   **Source of Truth:** Always treat the contents of the `src/` directory as the authoritative source for application logic, especially `crawler.py`, `index_builder.py`, and `search_docs.py`.

*,
*This guide was generated from the project structure, setup scripts, and module descriptions. See CLAUDE.md and phases.md for detailed information.*