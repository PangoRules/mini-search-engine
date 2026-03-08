# Mini Search Engine

A search engine built from scratch in Python — no frameworks, no magic. Just Python, SQLite, and fundamentals.

> Built as a learning journey. See [phases.md](./phases.md) for the full roadmap.

---

## What it does (so far)

- Loads `.txt` documents from a local `data/` folder
- Stores them in a SQLite database
- Tokenizes document content (lowercase, removes punctuation and stopwords)
- Builds an inverted index mapping tokens to documents with term frequency
- Searches documents by query and returns results ranked by term frequency
- Supports clearing and reinitializing the database

---

## Project Structure

```
mini-search-engine/
├── data/
│   └── sample_docs/        # Sample .txt documents
├── scripts/
│   ├── setup_db.py         # Initialize (and optionally clear) the SQLite database
│   └── load_sample_docs.py # Load sample docs into the database
├── src/
│   └── mini_search/
│       ├── config.py       # Paths and project config
│       ├── models.py       # Data models (Document)
│       ├── tokenizer.py    # Tokenization and normalization
│       ├── index_builder.py # Builds and persists the inverted index
│       ├── search_docs.py  # Search function with term frequency ranking
│       ├── storage/
│       │   ├── connection.py       # Database connection
│       │   ├── documents.py        # Document table queries
│       │   └── document_tokens.py  # Inverted index table queries
│       └── __init__.py
├── tests/                  # (coming in Phase 7)
├── phases.md               # Full build roadmap
└── README.md
```

---

## Setup

**Requirements:** Python 3.14+

```bash
# Clone the repo
git clone <repo-url>
cd mini-search-engine

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Initialize the database
python scripts/setup_db.py

# Load sample documents
python scripts/load_sample_docs.py

# Build the inverted index
python src/mini_search/index_builder.py

# Search!
python src/mini_search/search_docs.py
```

---

## Current Status

- **Phase 1 — Project Foundations** ✅
- **Phase 2 — Text Processing + Local Document Search** ✅
- Phase 3 — Web Crawling _(coming next)_

```bash
ruff check src/     # lint
black src/          # format
pytest tests/       # run tests
```

See [phases.md](./phases.md) for the full roadmap across all 7 phases.
