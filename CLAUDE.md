# Mini Search Engine - Claude Guide

## Project Goal
Build a mini search engine from scratch in Python — no frameworks, no magic. SQLite, fundamentals, and clean architecture.

## My Role
Act as a coworker, senior programmer, and architect. You can give code snippets and concrete implementations, but always explain the reasoning — why this structure, why this pattern, what trade-offs exist. Guide toward robust and scalable solutions without overengineering. Call out bad patterns, suggest better ones, and keep the codebase clean and consistent.

## Project Structure
```
mini-search-engine/
├── .venv/                          # Python 3.14 virtual environment
├── data/
│   ├── sample_docs/                # Sample .txt documents (Phase 2)
│   └── search_engine.db            # SQLite database
├── scripts/
│   ├── setup_db.py                 # Initialize (and optionally clear) the SQLite database
│   └── load_sample_docs.py         # Load sample docs into the database
├── src/
│   └── mini_search/
│       ├── __init__.py
│       ├── config.py               # Paths and project config
│       ├── models.py               # Data models: Document, ScrapedPage
│       ├── tokenizer.py            # Tokenization and normalization (complete)
│       ├── index_builder.py        # Inverted index builder for local docs (Phase 2)
│       ├── search_docs.py          # Search function for local docs (Phase 2)
│       ├── crawler.py              # Web crawler: BFS, robots.txt, domain filtering (Phase 3)
│       ├── pagerank.py             # PageRank authority scorer (Phase 5)
│       ├── search_scraped_pages.py # TF-IDF + combined search for crawled pages (Phase 5)
│       ├── utils/
│       │   ├── scrape_utils.py     # HTML scraping + ScrapedPageDto
│       │   └── url_utils.py        # URL normalization
│       └── storage/
│           ├── connection.py       # SQLite connection
│           ├── documents.py        # documents table CRUD (local docs)
│           ├── document_tokens.py  # document_tokens table CRUD (inverted index, local docs)
│           ├── scraped_pages.py    # scraped_pages table CRUD
│           └── scraped_page_tokens.py  # scraped_page_tokens table CRUD + index pipeline (Phase 4)
├── tests/                          # (Phase 7)
├── phases.md                       # Full build roadmap
└── README.md
```

## Environment
- Python 3.14
- Virtual environment at `.venv/` — user activates manually
- Package installed via `pyproject.toml` (editable install: `pip install -e .`)
- Run scripts from project root: `python scripts/setup_db.py`, `python src/mini_search/crawler.py`

## Current Phase
**Phase 6 — Search API + Pagination**

Expose the search engine via a FastAPI REST endpoint with pagination, ranked results, and basic rate limiting.

## Completed Phases
- Phase 1: Project foundations ✅
- Phase 2: Text processing + local document search ✅
- Phase 3: Web crawling ✅ (robots.txt, approved domains, dedup, depth/page limits)
- Phase 4: Indexing crawled pages ✅ (scraped_page_tokens table, flatten pipeline, batched index builder)
- Phase 5: Ranking ✅ (TF-IDF scorer, PageRank authority score, combined search_with_authority)

## Key Notes
- ALWAYS re-read files when the user references them or asks about their current state — never assume the file hasn't changed
- Scraped pages store tokenized content as JSON (paragraphs, headings, etc. are token lists) — no re-tokenization needed when reading from DB
- Separation of concerns: keep web index (`scraped_page_tokens`) separate from local doc index (`document_tokens`)
- Explain trade-offs and architectural decisions, don't just write code
