# Mini Search Engine

A search engine built from scratch in Python — no frameworks, no magic. Just Python, SQLite, and fundamentals.

> Built as a learning journey. See [phases.md](./phases.md) for the full roadmap.

---

## What it does (so far)

- Loads `.txt` documents from a local `data/` folder
- Stores them in a SQLite database
- Deduplicates on file path — safe to run multiple times

---

## Project Structure

```
mini-search-engine/
├── data/
│   └── sample_docs/        # Sample .txt documents
├── scripts/
│   ├── setup_db.py         # Initialize the SQLite database
│   └── load_sample_docs.py # Load sample docs into the database
├── src/
│   └── mini_search/
│       ├── config.py       # Paths and project config
│       ├── storage.py      # Database connection and queries
│       ├── models.py       # Data models (Document)
│       ├── tokenizer.py    # (coming in Phase 2)
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
```

---

## Current Status

**Phase 1 — Project Foundations** 

```bash
ruff check src/     # lint
black src/          # format
pytest tests/       # run tests
```

### Phase 2 — Text Processing + Local Document Search

**What to build**
- [ ] `tokenizer.py` — lowercase, remove punctuation, split into tokens, remove stopwords, optional stemming
- [ ] Inverted index builder — maps `word -> [doc_ids]`
- [ ] Search function — takes a query, returns matching documents
- [ ] Store index in SQLite or in-memory dict
- [ ] Basic ranking by term frequency

See [phases.md](./phases.md) for the full roadmap across all 7 phases.
