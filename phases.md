# Mini Search Engine

A search engine built from scratch as a Python learning journey.

---

## Phases

### Phase 1 — Project Foundations
> Set up the repo, Python environment, project structure, and mental model.

**Concepts to learn**
- Python project structure
- Virtual environments
- Package/dependency management
- Basic CLI scripts
- Reading/writing files
- SQLite basics
- Clean module separation

**Python to practice**
- Functions
- Classes (only where useful)
- Typing
- `pathlib`
- `sqlite3`
- List/dict/set basics
- Comprehensions
- `collections.Counter`
- Dataclasses
- Exceptions
- Modules/imports

**Deliverables**
- [X] Git repo initialized
- [x] Python virtual environment working
- [x] Linter/formatter/test setup
- [x] Folder structure created (`data/`, `scripts/`, `tests/`, `src/mini_search/`)
- [x] Modules scaffolded: `config.py`, `storage.py`, `tokenizer.py`, `models.py`
- [x] `scripts/setup_db.py` — initializes the SQLite database
- [x] `scripts/load_sample_docs.py` — reads text files and stores them in SQLite
- [x] This README

---

### Phase 2 — Text Processing + Local Document Search
> Understand the core of search without web crawling getting in the way.

**Concepts to learn**
- Tokenization
- Normalization (lowercase, punctuation removal)
- Stop words
- Stemming basics
- Term frequency
- Inverted indexes

**Python to practice**
- String methods
- `re` (regular expressions)
- `collections.Counter`
- Dictionaries as indexes
- File I/O
- Dataclasses or simple classes for document/token models

**What to build**
- [x] `tokenizer.py` — lowercase, remove punctuation, split into tokens, remove stopwords, optional stemming
- [x] Inverted index builder — maps `word -> [doc_ids]`
- [x] Search function — takes a query, returns matching documents
- [x] Store index in SQLite or in-memory dict
- [x] Basic ranking by term frequency
- [x] `clear_documents_table` and `clear_document_tokens_table` utility functions

**Mental model**

Given 3 docs:
```
Doc 1: "cats chase mice"
Doc 2: "dogs chase cats"
Doc 3: "mice hide"
```
Inverted index:
```
cats  -> [1, 2]
chase -> [1, 2]
mice  -> [1, 3]
dogs  -> [2]
hide  -> [3]
```

**Success checkpoint**
- [X] Type `cats chase` and get matching documents back in a sensible order

---

### Phase 3 — Web Crawling
> Learn how to collect documents from the web.

**Concepts to learn**
- HTTP requests
- HTML parsing
- Extracting links
- URL normalization
- Queue/frontier concepts
- Duplicate avoidance
- `robots.txt` awareness
- Crawl depth limiting

**Python/libraries to practice**
- `requests` or `httpx`
- `BeautifulSoup` (`bs4`)
- `urllib.parse`
- Sets for visited URL tracking
- Queues (`collections.deque`)

**What to build**
- [X] Crawler that starts from seed URLs
- [X] Fetches pages and extracts text + links
- [X] Normalizes URLs to avoid duplicates
- [x] Stores discovered pages in the database
- [x] Respects crawl constraints: approved domains only, max depth 2-3, max 100-500 pages, HTML only
- [X] robots.txt awareness
- [x] Approved domains only
- [X] URLs queued multiple times (in-queue deduplication)
- [x] main() arguments look swapped

**Success checkpoint**
- [x] Give it 2-3 seed URLs and it stores a small crawl set in the database

---

### Phase 4 — Indexing Crawled Pages
> Turn crawled pages into a searchable index.

**Concepts to learn**
- HTML text extraction (visible text only)
- Document metadata extraction (title, URL, headings)
- Term frequencies from real web pages
- Storing postings (index entries)
- Content deduplication
- Indexing pipeline design

**Python/libraries to practice**
- `BeautifulSoup` for text extraction
- SQLite for storing postings
- Pipeline pattern (functions chained together)

**What to build**
- [ ] Pipeline: crawled page -> extract text -> tokenize -> count terms -> store in index
- [ ] Store per document: URL, title, body text
- [ ] Index script that processes all crawled pages

**Success checkpoint**
- [ ] Run a script and see: crawl complete, index built, N documents indexed, M unique terms stored

---

### Phase 5 — Ranking
> Make results better than "just matches."

**Concepts to learn**
- TF-IDF (term frequency - inverse document frequency)
- BM25 basics
- PageRank intuition
- Link graph ideas
- Combining multiple scores

**Python to practice**
- Math (`math` module)
- Sorting with custom keys
- Weighted scoring functions
- Graph basics (dicts of dicts or `networkx`)

**What to build**
- [ ] TF-IDF scorer
- [ ] Basic PageRank-like authority score from link graph
- [ ] Combined ranking: text relevance + authority score

**Success checkpoint**
- [ ] Search results feel noticeably better than random matching order

---

### Phase 6 — Search API + Pagination
> Expose your search engine through a backend API.

**Concepts to learn**
- FastAPI basics
- Request/response models
- Query params
- Pagination design
- Error handling
- Rate limiting basics

**Python/libraries to practice**
- `fastapi`
- `pydantic`
- `uvicorn`
- In-memory rate limiting

**What to build**
- [ ] `GET /search?q=python&page=1&page_size=10`
- [ ] Response includes: query, total results, total pages, current page, results list
- [ ] Each result includes: title, URL, snippet, score
- [ ] Basic rate limiting

**Success checkpoint**
- [ ] Search via browser or Swagger UI and get paginated ranked results

---

### Phase 7 — Polish for Resume Quality
> Turn it from "it works" into "this is solid and professional."

**Concepts to learn**
- Testing with `pytest`
- Logging
- Docker basics
- Documentation
- Project storytelling

**Python/tools to practice**
- `pytest`
- `logging`
- `Dockerfile` + `docker-compose`
- Type hints throughout

**What to build**
- [ ] Tests: tokenizer, URL normalization, inverted index, scoring, pagination
- [ ] Structured logs with crawl stats and performance notes
- [ ] Per-domain `max_pages` limit in crawler (currently global limit causes uneven crawling across domains)
- [ ] Docker setup so anyone can run it
- [ ] Architecture diagram
- [ ] Clean README with setup instructions, known limitations, future improvements
- [ ] Sample data/seed instructions

**Success checkpoint**
- [ ] Someone can clone the repo, run it, and understand what it does without asking you anything
